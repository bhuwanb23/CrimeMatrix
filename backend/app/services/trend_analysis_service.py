import json
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func, extract
from app.models.crime import Crime
from app.models.district import District
from app.models.crimetype import CrimeType
from app.models.crime_statistic import CrimeStatistic
from app.models.trend_snapshot import TrendSnapshot
import structlog
from datetime import datetime, timedelta
from collections import defaultdict

logger = structlog.get_logger()


class TrendAnalysisService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_summary(self, period: str = "daily", district_id: int = None,
                          crime_type_id: int = None, days: int = 30) -> dict:
        date_from = datetime.utcnow() - timedelta(days=days)
        date_prev = date_from - timedelta(days=days)

        current = await self._get_crime_counts(date_from, None, district_id, crime_type_id)
        previous = await self._get_crime_counts(date_prev, date_from, district_id, crime_type_id)

        total_current = sum(c["count"] for c in current)
        total_previous = sum(c["count"] for c in previous)

        change_pct = ((total_current - total_previous) / max(total_previous, 1)) * 100
        direction = "up" if change_pct > 5 else "down" if change_pct < -5 else "stable"

        peak = max(current, key=lambda x: x["count"]) if current else {"date": "N/A", "count": 0}
        low = min(current, key=lambda x: x["count"]) if current else {"date": "N/A", "count": 0}

        return {
            "total_crimes": total_current,
            "previous_total": total_previous,
            "change_pct": round(change_pct, 1),
            "direction": direction,
            "peak": peak,
            "low": low,
            "period": period,
            "days": days,
        }

    async def get_daily_trends(self, days: int = 30, district_id: int = None,
                               crime_type_id: int = None) -> dict:
        date_from = datetime.utcnow() - timedelta(days=days)
        data = await self._get_crime_counts(date_from, None, district_id, crime_type_id)
        return {"period": "daily", "data": data, "total": sum(d["count"] for d in data)}

    async def get_weekly_trends(self, weeks: int = 12, district_id: int = None,
                                crime_type_id: int = None) -> dict:
        date_from = datetime.utcnow() - timedelta(weeks=weeks)
        query = select(
            sql_func.strftime("%Y-%W", Crime.created_at).label("week"),
            sql_func.count(Crime.id).label("count")
        ).where(Crime.created_at >= date_from)
        if district_id:
            query = query.where(Crime.district_id == district_id)
        if crime_type_id:
            query = query.where(Crime.crime_type_id == crime_type_id)
        query = query.group_by("week").order_by("week")
        result = await self.db.execute(query)
        data = [{"period": r[0], "count": r[1]} for r in result.all()]
        return {"period": "weekly", "data": data, "total": sum(d["count"] for d in data)}

    async def get_monthly_trends(self, months: int = 12, district_id: int = None,
                                 crime_type_id: int = None) -> dict:
        date_from = datetime.utcnow() - timedelta(days=months * 30)
        query = select(
            sql_func.strftime("%Y-%m", Crime.created_at).label("month"),
            sql_func.count(Crime.id).label("count")
        ).where(Crime.created_at >= date_from)
        if district_id:
            query = query.where(Crime.district_id == district_id)
        if crime_type_id:
            query = query.where(Crime.crime_type_id == crime_type_id)
        query = query.group_by("month").order_by("month")
        result = await self.db.execute(query)
        data = [{"period": r[0], "count": r[1]} for r in result.all()]
        return {"period": "monthly", "data": data, "total": sum(d["count"] for d in data)}

    async def get_yearly_trends(self, years: int = 5) -> dict:
        date_from = datetime.utcnow() - timedelta(days=years * 365)
        query = select(
            sql_func.strftime("%Y", Crime.created_at).label("year"),
            sql_func.count(Crime.id).label("count")
        ).where(Crime.created_at >= date_from)
        query = query.group_by("year").order_by("year")
        result = await self.db.execute(query)
        data = [{"period": r[0], "count": r[1]} for r in result.all()]
        return {"period": "yearly", "data": data, "total": sum(d["count"] for d in data)}

    async def get_district_trends(self, district_id: int, days: int = 30) -> dict:
        date_from = datetime.utcnow() - timedelta(days=days)
        data = await self._get_crime_counts(date_from, None, district_id)
        district = await self._load_district(district_id)
        return {
            "district": district,
            "data": data,
            "total": sum(d["count"] for d in data),
        }

    async def compare_districts(self, district_ids: List[int], days: int = 30) -> dict:
        date_from = datetime.utcnow() - timedelta(days=days)
        result = {}
        for did in district_ids:
            data = await self._get_crime_counts(date_from, None, did)
            district = await self._load_district(did)
            name = district.get("name", f"District #{did}") if district else f"District #{did}"
            result[name] = {"data": data, "total": sum(d["count"] for d in data)}
        return {"districts": result, "days": days}

    async def get_seasonal_patterns(self, days: int = 365) -> dict:
        date_from = datetime.utcnow() - timedelta(days=days)

        hour_query = select(
            extract("hour", Crime.created_at).label("hour"),
            sql_func.count(Crime.id).label("count")
        ).where(Crime.created_at >= date_from).group_by("hour").order_by("hour")
        hour_result = await self.db.execute(hour_query)
        by_hour = [{"hour": int(r[0]) if r[0] else 0, "count": r[1]} for r in hour_result.all()]

        dow_query = select(
            sql_func.strftime("%w", Crime.created_at).label("dow"),
            sql_func.count(Crime.id).label("count")
        ).where(Crime.created_at >= date_from).group_by("dow").order_by("dow")
        dow_result = await self.db.execute(dow_query)
        dow_labels = {0: "Sun", 1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat"}
        by_dow = [{"day": dow_labels.get(int(r[0]), r[0]), "count": r[1]} for r in dow_result.all()]

        month_query = select(
            sql_func.strftime("%m", Crime.created_at).label("month"),
            sql_func.count(Crime.id).label("count")
        ).where(Crime.created_at >= date_from).group_by("month").order_by("month")
        month_result = await self.db.execute(month_query)
        month_labels = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
        by_month = [{"month": month_labels.get(int(r[0]), r[0]), "count": r[1]} for r in month_result.all()]

        return {"by_hour": by_hour, "by_day_of_week": by_dow, "by_month": by_month}

    async def get_crime_type_trends(self, days: int = 30) -> dict:
        date_from = datetime.utcnow() - timedelta(days=days)
        query = select(
            CrimeType.name,
            sql_func.count(Crime.id).label("count")
        ).join(Crime, Crime.crime_type_id == CrimeType.id).where(Crime.created_at >= date_from)
        query = query.group_by(CrimeType.name).order_by(sql_func.count(Crime.id).desc())
        result = await self.db.execute(query)
        return {"data": [{"type": r[0], "count": r[1]} for r in result.all()]}

    async def create_snapshot(self, metric_name: str, metric_value: float,
                              comparison_value: float = None) -> dict:
        change_pct = None
        direction = None
        if comparison_value and comparison_value > 0:
            change_pct = ((metric_value - comparison_value) / comparison_value) * 100
            direction = "up" if change_pct > 5 else "down" if change_pct < -5 else "stable"

        snapshot = TrendSnapshot(
            snapshot_date=datetime.utcnow(),
            metric_name=metric_name,
            metric_value=metric_value,
            comparison_value=comparison_value,
            change_pct=round(change_pct, 1) if change_pct else None,
            direction=direction,
        )
        self.db.add(snapshot)
        await self.db.commit()
        return {"id": snapshot.id, "metric_name": metric_name, "metric_value": metric_value}

    async def get_snapshots(self, metric_name: str = None, limit: int = 30) -> List[dict]:
        stmt = select(TrendSnapshot)
        if metric_name:
            stmt = stmt.where(TrendSnapshot.metric_name == metric_name)
        stmt = stmt.order_by(TrendSnapshot.snapshot_date.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return [
            {"id": s.id, "metric_name": s.metric_name, "metric_value": s.metric_value,
             "change_pct": s.change_pct, "direction": s.direction,
             "snapshot_date": str(s.snapshot_date) if s.snapshot_date else None}
            for s in result.scalars().all()
        ]

    async def _get_crime_counts(self, date_from, date_to, district_id=None, crime_type_id=None) -> List[dict]:
        query = select(
            sql_func.date(Crime.created_at).label("date"),
            sql_func.count(Crime.id).label("count")
        ).where(Crime.created_at >= date_from)
        if date_to:
            query = query.where(Crime.created_at <= date_to)
        if district_id:
            query = query.where(Crime.district_id == district_id)
        if crime_type_id:
            query = query.where(Crime.crime_type_id == crime_type_id)
        query = query.group_by("date").order_by("date")
        result = await self.db.execute(query)
        return [{"date": str(r[0]) if r[0] else "unknown", "count": r[1]} for r in result.all()]

    async def _load_district(self, district_id: int) -> Optional[dict]:
        stmt = select(District).where(District.id == district_id)
        result = await self.db.execute(stmt)
        d = result.scalar()
        return {"id": d.id, "name": d.name} if d else None
