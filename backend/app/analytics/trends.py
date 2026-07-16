from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.crime import Crime
from typing import Optional
import structlog

logger = structlog.get_logger()


class TrendEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def crime_trends(
        self, period: str = "daily", start_date: str = None, end_date: str = None
    ) -> dict:
        query = select(Crime.created_at, func.count(Crime.id))

        if start_date:
            query = query.where(Crime.created_at >= start_date)
        if end_date:
            query = query.where(Crime.created_at <= end_date)

        query = query.group_by(Crime.created_at).order_by(Crime.created_at)
        result = await self.db.execute(query)
        rows = result.all()

        data = [{"date": str(row[0])[:10] if row[0] else "unknown", "count": row[1]} for row in rows]
        return {"period": period, "data": data}

    async def case_trends(
        self, start_date: str = None, end_date: str = None
    ) -> dict:
        query = select(Crime.status, func.count(Crime.id))

        if start_date:
            query = query.where(Crime.created_at >= start_date)
        if end_date:
            query = query.where(Crime.created_at <= end_date)

        query = query.group_by(Crime.status)
        result = await self.db.execute(query)
        rows = result.all()

        data = [{"status": row[0] or "unknown", "count": row[1]} for row in rows]
        return {"data": data}

    async def resolution_trend(self) -> dict:
        total = (await self.db.execute(select(func.count(Crime.id)))).scalar() or 0
        resolved = (await self.db.execute(
            select(func.count(Crime.id)).where(Crime.status == "closed")
        )).scalar() or 0

        rate = round((resolved / total * 100), 1) if total > 0 else 0

        return {
            "total": total,
            "resolved": resolved,
            "pending": total - resolved,
            "resolution_rate": rate,
        }
