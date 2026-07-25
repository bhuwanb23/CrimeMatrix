import json
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func, extract
from app.models.crime import Crime
from app.models.district import District
from app.models.crime_forecast_record import CrimeForecastRecord
from app.models.forecast_snapshot import ForecastSnapshot
import structlog
from datetime import datetime, timedelta
from collections import defaultdict
import math

logger = structlog.get_logger()


class ForecastService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def forecast_district(self, district_id: int, periods: int = 30) -> dict:
        date_from = datetime.utcnow() - timedelta(days=periods * 2)
        date_col = sql_func.coalesce(Crime.occurred_at, Crime.created_at)
        stmt = select(
            sql_func.date(date_col).label("date"),
            sql_func.count(Crime.id).label("count")
        ).where(Crime.district_id == district_id, date_col >= date_from)
        stmt = stmt.group_by(sql_func.date(date_col)).order_by(sql_func.date(date_col))
        result = await self.db.execute(stmt)
        data = [{"date": str(r[0]) if r[0] else "unknown", "count": r[1]} for r in result.all()]

        forecast_result = self._compute_forecast(data, periods)
        district = await self._load_district(district_id)

        for f in forecast_result["predictions"]:
            rec = CrimeForecastRecord(
                forecast_type="district", district_id=district_id,
                predicted_value=f["count"], confidence=forecast_result["confidence"],
                target_period=f.get("date", ""), model_name="moving_average",
            )
            self.db.add(rec)
        await self.db.commit()

        return {"district": district, "historical": data, "forecast": forecast_result["predictions"],
                "trend": forecast_result["trend"], "confidence": forecast_result["confidence"],
                "data_points": forecast_result["data_points"]}

    async def forecast_category(self, crime_type_id: int, periods: int = 30) -> dict:
        date_from = datetime.utcnow() - timedelta(days=periods * 2)
        date_col = sql_func.coalesce(Crime.occurred_at, Crime.created_at)
        stmt = select(
            sql_func.date(date_col).label("date"),
            sql_func.count(Crime.id).label("count")
        ).where(Crime.crime_type_id == crime_type_id, date_col >= date_from)
        stmt = stmt.group_by(sql_func.date(date_col)).order_by(sql_func.date(date_col))
        result = await self.db.execute(stmt)
        data = [{"date": str(r[0]) if r[0] else "unknown", "count": r[1]} for r in result.all()]

        forecast_result = self._compute_forecast(data, periods)

        return {"crime_type_id": crime_type_id, "historical": data,
                "forecast": forecast_result["predictions"], "trend": forecast_result["trend"],
                "confidence": forecast_result["confidence"], "data_points": forecast_result["data_points"]}

    async def get_seasonal_patterns(self, days: int = 365) -> dict:
        date_from = datetime.utcnow() - timedelta(days=days)
        date_col = sql_func.coalesce(Crime.occurred_at, Crime.created_at)

        # By hour
        hour_stmt = select(
            extract("hour", date_col).label("hour"),
            sql_func.count(Crime.id).label("count")
        ).where(date_col >= date_from).group_by("hour").order_by("hour")
        hour_result = await self.db.execute(hour_stmt)
        by_hour = [{"hour": int(r[0]) if r[0] else 0, "count": r[1]} for r in hour_result.all()]

        # By day of week
        dow_stmt = select(
            sql_func.strftime("%w", date_col).label("dow"),
            sql_func.count(Crime.id).label("count")
        ).where(date_col >= date_from).group_by("dow").order_by("dow")
        dow_result = await self.db.execute(dow_stmt)
        dow_labels = {"0": "Sun", "1": "Mon", "2": "Tue", "3": "Wed", "4": "Thu", "5": "Fri", "6": "Sat"}
        by_dow = [{"day": dow_labels.get(str(r[0]), str(r[0])), "count": r[1]} for r in dow_result.all()]

        # By month
        month_stmt = select(
            sql_func.strftime("%m", date_col).label("month"),
            sql_func.count(Crime.id).label("count")
        ).where(date_col >= date_from).group_by("month").order_by("month")
        month_result = await self.db.execute(month_stmt)
        month_labels = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun",
                         "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
        by_month = [{"month": month_labels.get(str(r[0]).zfill(2), str(r[0])), "count": r[1]} for r in month_result.all()]

        return {"by_hour": by_hour, "by_day_of_week": by_dow, "by_month": by_month}

    async def get_forecast_history(self, limit: int = 30) -> list:
        stmt = select(CrimeForecastRecord).order_by(CrimeForecastRecord.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return [{"id": f.id, "forecast_type": f.forecast_type, "predicted_value": f.predicted_value,
                 "confidence": f.confidence, "target_period": f.target_period, "model_name": f.model_name,
                 "created_at": str(f.created_at) if f.created_at else None} for f in result.scalars().all()]

    async def get_forecast_stats(self) -> dict:
        total = (await self.db.execute(select(sql_func.count(CrimeForecastRecord.id)))).scalar() or 0
        avg_conf = (await self.db.execute(select(sql_func.avg(CrimeForecastRecord.confidence)))).scalar()
        return {"total_forecasts": total, "avg_confidence": round(avg_conf or 0, 1)}

    def _compute_forecast(self, data: list, periods: int) -> dict:
        if len(data) < 2:
            return {"predictions": [], "trend": "stable", "confidence": 0, "data_points": len(data)}

        counts = [d["count"] for d in data]
        avg = sum(counts) / len(counts)
        recent = counts[-7:] if len(counts) >= 7 else counts
        recent_avg = sum(recent) / len(recent)
        earlier = counts[:max(len(counts) - 7, 1)]
        earlier_avg = sum(earlier) / len(earlier) if earlier else recent_avg

        change_pct = ((recent_avg - earlier_avg) / max(earlier_avg, 1)) * 100
        trend = "increasing" if change_pct > 5 else "decreasing" if change_pct < -5 else "stable"

        predictions = []
        for i in range(1, min(periods, 30) + 1):
            predicted = round(avg + (change_pct / 100 * avg * i / periods))
            predictions.append({"date": f"day_{i}", "count": max(0, predicted), "confidence": max(40, 85 - i * 2)})

        confidence = min(95, max(40, 60 + len(data) * 2))

        return {"predictions": predictions, "trend": trend, "confidence": confidence, "data_points": len(data)}

    async def _load_district(self, district_id: int) -> Optional[dict]:
        stmt = select(District).where(District.id == district_id)
        result = await self.db.execute(stmt)
        d = result.scalar()
        return {"id": d.id, "name": d.name, "code": d.code} if d else None
