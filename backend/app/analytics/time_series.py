from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, String
from app.models.crime import Crime
import structlog

logger = structlog.get_logger()


class TimeSeriesEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _day_expr(self, date_col):
        # Portable day bucket: cast to string and slice in Python if dialect lacks strftime
        return cast(date_col, String)

    async def crime_series(self, start_date: str = None, end_date: str = None) -> list:
        date_col = func.coalesce(Crime.occurred_at, Crime.created_at)
        query = select(date_col, func.count(Crime.id))

        if start_date:
            query = query.where(date_col >= start_date)
        if end_date:
            query = query.where(date_col <= end_date)

        query = query.group_by(date_col).order_by(date_col)
        try:
            result = await self.db.execute(query)
            buckets: dict[str, int] = {}
            for row in result.all():
                day = str(row[0])[:10] if row[0] else "unknown"
                buckets[day] = buckets.get(day, 0) + int(row[1] or 0)
            return [{"date": d, "value": v} for d, v in sorted(buckets.items())]
        except Exception as e:
            logger.warning("crime_series_failed", error=str(e))
            return []

    async def case_series(self, start_date: str = None, end_date: str = None) -> list:
        query = select(Crime.status, func.count(Crime.id))

        if start_date:
            query = query.where(Crime.created_at >= start_date)
        if end_date:
            query = query.where(Crime.created_at <= end_date)

        query = query.group_by(Crime.status)
        try:
            result = await self.db.execute(query)
            return [
                {"date": row[0] or "unknown", "value": row[1]}
                for row in result.all()
            ]
        except Exception as e:
            logger.warning("case_series_failed", error=str(e))
            return []

    async def activity_series(self, start_date: str = None, end_date: str = None) -> list:
        date_col = func.coalesce(Crime.occurred_at, Crime.created_at)
        crime_query = select(date_col, func.count(Crime.id))
        if start_date:
            crime_query = crime_query.where(date_col >= start_date)
        if end_date:
            crime_query = crime_query.where(date_col <= end_date)
        crime_query = crime_query.group_by(date_col).order_by(date_col)
        try:
            crimes = await self.db.execute(crime_query)
            series = {}
            for date_val, count in crimes.all():
                date_str = str(date_val)[:10] if date_val else "unknown"
                if date_str not in series:
                    series[date_str] = {"date": date_str, "crimes": 0, "total": 0}
                series[date_str]["crimes"] = count
                series[date_str]["total"] += count
            return sorted(series.values(), key=lambda x: x["date"])
        except Exception as e:
            logger.warning("activity_series_failed", error=str(e))
            return []
