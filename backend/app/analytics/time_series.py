from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.crime import Crime
import structlog

logger = structlog.get_logger()


class TimeSeriesEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def crime_series(self, start_date: str = None, end_date: str = None) -> list:
        query = select(Crime.created_at, func.count(Crime.id))

        if start_date:
            query = query.where(Crime.created_at >= start_date)
        if end_date:
            query = query.where(Crime.created_at <= end_date)

        query = query.group_by(Crime.created_at).order_by(Crime.created_at)
        result = await self.db.execute(query)

        return [
            {"date": str(row[0])[:10] if row[0] else "unknown", "value": row[1]}
            for row in result.all()
        ]

    async def case_series(self, start_date: str = None, end_date: str = None) -> list:
        query = select(Crime.status, func.count(Crime.id))

        if start_date:
            query = query.where(Crime.created_at >= start_date)
        if end_date:
            query = query.where(Crime.created_at <= end_date)

        query = query.group_by(Crime.status)
        result = await self.db.execute(query)

        return [
            {"date": row[0] or "unknown", "value": row[1]}
            for row in result.all()
        ]

    async def activity_series(self, start_date: str = None, end_date: str = None) -> list:
        crime_query = select(Crime.created_at, func.count(Crime.id))
        if start_date:
            crime_query = crime_query.where(Crime.created_at >= start_date)
        if end_date:
            crime_query = crime_query.where(Crime.created_at <= end_date)
        crime_query = crime_query.group_by(Crime.created_at).order_by(Crime.created_at)
        crimes = await self.db.execute(crime_query)

        series = {}
        for date_val, count in crimes.all():
            date_str = str(date_val)[:10] if date_val else "unknown"
            if date_str not in series:
                series[date_str] = {"date": date_str, "crimes": 0, "total": 0}
            series[date_str]["crimes"] = count
            series[date_str]["total"] += count

        return sorted(series.values(), key=lambda x: x["date"])
