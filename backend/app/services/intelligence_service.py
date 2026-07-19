from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.crime import Crime
from app.models.crimetype import CrimeType
from app.models.district import District
from app.models.criminal import Criminal
from app.models.victim import Victim
from app.models.witness import Witness
from app.models.investigation import Investigation
from app.analytics.trends import TrendEngine
from app.analytics.districts import DistrictAnalytics
from app.analytics.heatmaps import HeatmapEngine
import structlog
from datetime import datetime, timedelta

logger = structlog.get_logger()


class IntelligenceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.trends = TrendEngine(db)
        self.districts = DistrictAnalytics(db)
        self.heatmaps = HeatmapEngine(db)

    async def get_summary(self, district: str = None, time_range: str = "30d",
                          crime_type: str = None) -> dict:
        overview = await self._get_overview(district, time_range, crime_type)
        trends = await self._get_trends(time_range)
        hotspots = await self._get_hotspots(time_range)
        criminal_activity = await self._get_criminal_activity(time_range)
        ai_insights = await self._get_ai_insights(overview, trends, hotspots)

        return {
            "overview": overview,
            "trends": trends,
            "hotspots": hotspots,
            "criminal_activity": criminal_activity,
            "ai_insights": ai_insights,
            "filters": {
                "district": district,
                "time_range": time_range,
                "crime_type": crime_type,
            },
        }

    async def _get_overview(self, district: str = None, time_range: str = "30d",
                            crime_type: str = None) -> dict:
        date_from = self._get_date_from(time_range)

        query = select(sql_func.count(Crime.id))
        if date_from:
            query = query.where(Crime.created_at >= date_from)
        if crime_type:
            query = query.where(Crime.crime_type_id.isnot(None))
        total = (await self.db.execute(query)).scalar() or 0

        open_q = select(sql_func.count(Crime.id)).where(Crime.status == "open")
        if date_from:
            open_q = open_q.where(Crime.created_at >= date_from)
        open_count = (await self.db.execute(open_q)).scalar() or 0

        closed_q = select(sql_func.count(Crime.id)).where(Crime.status == "closed")
        if date_from:
            closed_q = closed_q.where(Crime.created_at >= date_from)
        closed_count = (await self.db.execute(closed_q)).scalar() or 0

        active_inv = (await self.db.execute(
            select(sql_func.count(Investigation.id)).where(Investigation.status == "active")
        )).scalar() or 0

        criminal_count = (await self.db.execute(
            select(sql_func.count(Criminal.id))
        )).scalar() or 0

        victim_count = (await self.db.execute(
            select(sql_func.count(Victim.id))
        )).scalar() or 0

        return {
            "total_crimes": total,
            "open_crimes": open_count,
            "closed_crimes": closed_count,
            "resolution_rate": round((closed_count / total * 100), 1) if total else 0,
            "active_investigations": active_inv,
            "active_criminals": criminal_count,
            "total_victims": victim_count,
        }

    async def _get_trends(self, time_range: str) -> dict:
        date_from = self._get_date_from(time_range)

        query = select(
            sql_func.date(Crime.created_at).label("day"),
            sql_func.count(Crime.id).label("count")
        )
        if date_from:
            query = query.where(Crime.created_at >= date_from)
        query = query.group_by(sql_func.date(Crime.created_at)).order_by(sql_func.date(Crime.created_at))
        result = await self.db.execute(query)
        rows = result.all()

        daily = [{"date": str(r[0]) if r[0] else "unknown", "count": r[1]} for r in rows]

        if len(daily) >= 2:
            recent = sum(d["count"] for d in daily[-7:]) / min(7, len(daily[-7:]))
            earlier = sum(d["count"] for d in daily[:7]) / min(7, len(daily[:7])) if daily[:7] else 1
            change = ((recent - earlier) / max(earlier, 1)) * 100
            direction = "up" if change > 5 else "down" if change < -5 else "stable"
        else:
            change = 0
            direction = "stable"

        return {
            "daily": daily,
            "direction": direction,
            "change_pct": round(change, 1),
            "period": time_range,
        }

    async def _get_hotspots(self, time_range: str) -> dict:
        date_from = self._get_date_from(time_range)

        query = select(
            Crime.district_id,
            sql_func.count(Crime.id).label("count")
        )
        if date_from:
            query = query.where(Crime.created_at >= date_from)
        query = query.group_by(Crime.district_id).order_by(sql_func.count(Crime.id).desc()).limit(5)
        result = await self.db.execute(query)
        rows = result.all()

        districts = []
        for row in rows:
            district_name = "Unknown"
            if row[0]:
                d_result = await self.db.execute(select(District.name).where(District.id == row[0]))
                d_name = d_result.scalar()
                if d_name:
                    district_name = d_name
            districts.append({"name": district_name, "count": row[1]})

        type_query = select(
            CrimeType.name,
            sql_func.count(Crime.id).label("count")
        )
        if date_from:
            type_query = type_query.join(Crime, Crime.crime_type_id == CrimeType.id).where(Crime.created_at >= date_from)
        else:
            type_query = type_query.join(Crime, Crime.crime_type_id == CrimeType.id)
        type_query = type_query.group_by(CrimeType.name).order_by(sql_func.count(Crime.id).desc()).limit(5)
        type_result = await self.db.execute(type_query)
        type_rows = type_result.all()

        return {
            "districts": districts,
            "top_crime_types": [{"name": r[0], "count": r[1]} for r in type_rows],
        }

    async def _get_criminal_activity(self, time_range: str) -> dict:
        active = (await self.db.execute(
            select(sql_func.count(Criminal.id)).where(Criminal.status == "active")
        )).scalar() or 0

        high_risk = (await self.db.execute(
            select(sql_func.count(Criminal.id)).where(Criminal.risk_score > 0.7)
        )).scalar() or 0

        victims = (await self.db.execute(select(sql_func.count(Victim.id)))).scalar() or 0
        witnesses = (await self.db.execute(select(sql_func.count(Witness.id)))).scalar() or 0

        return {
            "active_criminals": active,
            "high_risk_offenders": high_risk,
            "total_victims": victims,
            "total_witnesses": witnesses,
        }

    async def _get_ai_insights(self, overview: dict, trends: dict, hotspots: dict) -> dict:
        insights = []
        alerts = []

        if trends.get("direction") == "up" and trends.get("change_pct", 0) > 10:
            alerts.append({
                "type": "trend_up",
                "severity": "high",
                "message": f"Crime rate increased by {trends['change_pct']}% — requires attention",
            })

        if overview.get("resolution_rate", 0) < 50:
            alerts.append({
                "type": "low_resolution",
                "severity": "medium",
                "message": f"Resolution rate at {overview['resolution_rate']}% — below 50% target",
            })

        top_districts = hotspots.get("districts", [])
        if top_districts and top_districts[0].get("count", 0) > 10:
            alerts.append({
                "type": "hotspot",
                "severity": "high",
                "message": f"{top_districts[0]['name']} has {top_districts[0]['count']} crimes — hotspot detected",
            })

        if overview.get("active_investigations", 0) > 0:
            insights.append(
                f"{overview['active_investigations']} active investigations across all districts"
            )

        top_types = hotspots.get("top_crime_types", [])
        if top_types:
            insights.append(
                f"Most common crime type: {top_types[0]['name']} ({top_types[0]['count']} cases)"
            )

        return {
            "summary": f"System monitoring {overview.get('total_crimes', 0)} crimes across all districts. "
                       f"Resolution rate: {overview.get('resolution_rate', 0)}%. "
                       f"Trend: {trends.get('direction', 'stable')} ({trends.get('change_pct', 0)}%).",
            "alerts": alerts,
            "insights": insights,
        }

    def _get_date_from(self, time_range: str) -> Optional[datetime]:
        now = datetime.utcnow()
        if time_range == "7d":
            return now - timedelta(days=7)
        elif time_range == "30d":
            return now - timedelta(days=30)
        elif time_range == "90d":
            return now - timedelta(days=90)
        elif time_range == "1y":
            return now - timedelta(days=365)
        return None
