import json
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func, extract
from app.models.crime import Crime
from app.models.district import District
from app.models.crimetype import CrimeType
from app.models.crime_forecast_record import CrimeForecastRecord
from app.models.forecast_snapshot import ForecastSnapshot
import structlog
from datetime import datetime, timedelta
from collections import defaultdict

logger = structlog.get_logger()


class ForecastService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def forecast_district(self, district_id: int, periods: int = 30) -> dict:
        date_from = datetime.utcnow() - timedelta(days=periods * 2)
        stmt = select(
            sql_func.date(Crime.created_at).label("date"),
            sql_func.count(Crime.id).label("count")
        ).where(Crime.district_id == district_id, Crime.created_at >= date_from)
        stmt = stmt.group_by(sql_func.date(Crime.created_at)).order_by(sql_func.date(Crime.created_at))
        result = await self.db.execute(stmt)
        data = [{"date": str(r[0]) if r[0] else "unknown", "count": r[1]} for r in result.all()]

        forecast_result = self._compute_forecast(data, periods)
        district = await self._load_district(district_id)

        # Save forecast
        for f in forecast_result["predictions"]:
            rec = CrimeForecastRecord(
                forecast_type="district",
                district_id=district_id,
                predicted_value=f["count"],
                confidence=forecast_result["confidence"],
                target_period=f.get("date", ""),
                model_name="moving_average",
            )
            self.db.add(rec)
        await self.db.commit()

        return {
            "district": district,
            "historical": data,
            "forecast": forecast_result["predictions"],
            "trend": forecast_result["trend"],
            "confidence": forecast_result["confidence"],
            "data_points": forecast_result["data_points"],
        }

    async def forecast_category(self, crime_type_id: int, periods: int = 30) -> dict:
        date_from = datetime.utcnow() - timedelta(days=periods * 2)
        stmt = select(
            sql_func.date(Crime.created_at).label("date"),
            sql_func.count(Crime.id).label("count")
        ).where(Crime.crime_type_id == crime_type_id, Crime.created_at >= date_from)
        stmt = stmt.group_by(sql_func.date(Crime.created_at)).order_by(sql_func.date(Crime.created_at))
        result = await self.db.execute(stmt)
        data = [{"date": str(r[0]) if r[0] else "unknown", "count": r[1]} for r in result.all()]

        forecast_result = self._compute_forecast(data, periods)

        return {
            "crime_type_id": crime_type_id,
            "historical": data,
            "forecast": forecast_result["predictions"],
            "trend": forecast_result["trend"],
            "confidence": forecast_result["confidence"],
            "data_points": forecast_result["data_points"],
        }

    async def get_seasonal_patterns(self, days: int = 365) -> dict:
        date_from = datetime.utcnow() - timedelta(days=days)

        # By hour
        hour_stmt = select(
            extract("hour", Crime.created_at).label("hour"),
            sql_func.count(Crime.id).label("count")
        ).where(Crime.created_at >= date_from).group_by("hour").order_by("hour")
        hour_result = await self.db.execute(hour_stmt)
        by_hour = [{"hour": int(r[0]) if r[0] else 0, "count": r[1]} for r in hour_result.all()]

        # By day of week
        dow_stmt = select(
            sql_func.strftime("%w", Crime.created_at).label("dow"),
            sql_func.count(Crime.id).label("count")
        ).where(Crime.created_at >= date_from).group_by("dow").order_by("dow")
        dow_result = await self.db.execute(dow_stmt)
        dow_labels = {0: "Sun", 1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat"}
        by_dow = [{"day": dow_labels.get(int(r[0]), r[0]), "count": r[1]} for r in dow_result.all()]

        # By month
        month_stmt = select(
            sql_func.strftime("%m", Crime.created_at).label("month"),
            sql_func.count(Crime.id).label("count")
        ).where(Crime.created_at >= date_from).group_by("month").order_by("month")
        month_result = await self.db.execute(month_stmt)
        month_labels = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
        by_month = [{"month": month_labels.get(int(r[0]), r[0]), "count": r[1]} for r in month_result.all()]

        return {"by_hour": by_hour, "by_day_of_week": by_dow, "by_month": by_month}

    async def get_forecast_history(self, limit: int = 30) -> List[dict]:
        stmt = select(ForecastSnapshot).order_by(ForecastSnapshot.snapshot_date.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return [
            {"metric_name": s.metric_name, "metric_value": s.metric_value,
             "forecast_value": s.forecast_value, "confidence": s.confidence,
             "snapshot_date": str(s.snapshot_date) if s.snapshot_date else None}
            for s in result.scalars().all()
        ]

    async def get_forecast_stats(self) -> dict:
        total = (await self.db.execute(select(sql_func.count(CrimeForecastRecord.id)))).scalar() or 0
        districts = (await self.db.execute(
            select(sql_func.count(sql_func.distinct(CrimeForecastRecord.district_id)))
        )).scalar() or 0
        avg_conf = (await self.db.execute(select(sql_func.avg(CrimeForecastRecord.confidence)))).scalar()
        return {"total_forecasts": total, "districts_covered": districts, "avg_confidence": round(avg_conf or 0, 1)}

    def _compute_forecast(self, data: List[dict], periods: int) -> dict:
        if len(data) < 2:
            return {"predictions": [], "trend": "stable", "confidence": 10, "data_points": len(data)}

        counts = [d["count"] for d in data]
        n = len(counts)
        avg = sum(counts) / n
        recent = counts[-7:] if n >= 7 else counts
        recent_avg = sum(recent) / len(recent)

        if n >= 3:
            slope = (counts[-1] - counts[-3]) / 2
        else:
            slope = counts[-1] - counts[0]

        predictions = []
        for i in range(1, periods + 1):
            predicted = max(0, round(recent_avg + slope * i))
            predictions.append({
                "day": i,
                "date": (datetime.utcnow() + timedelta(days=i)).strftime("%Y-%m-%d"),
                "predicted": predicted,
            })

        trend = "increasing" if slope > 0.5 else "decreasing" if slope < -0.5 else "stable"
        variance = sum((x - avg) ** 2 for x in counts) / n
        confidence = min(100, max(10, int(80 - variance * 2)))

        return {
            "predictions": predictions,
            "trend": trend,
            "confidence": confidence,
            "data_points": n,
        }

    async def _load_district(self, district_id: int) -> Optional[dict]:
        stmt = select(District).where(District.id == district_id)
        result = await self.db.execute(stmt)
        d = result.scalar()
        return {"id": d.id, "name": d.name} if d else None
