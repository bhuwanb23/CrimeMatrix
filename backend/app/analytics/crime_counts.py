from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.crime import Crime
import structlog

logger = structlog.get_logger()


class CrimeCountEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def count_by_type(self) -> list:
        result = await self.db.execute(
            select(Crime.crime_type, func.count(Crime.id))
            .group_by(Crime.crime_type)
            .order_by(func.count(Crime.id).desc())
        )
        return [{"key": row[0] or "unknown", "value": row[1]} for row in result.all()]

    async def count_by_status(self) -> list:
        result = await self.db.execute(
            select(Crime.status, func.count(Crime.id))
            .group_by(Crime.status)
            .order_by(func.count(Crime.id).desc())
        )
        return [{"key": row[0] or "unknown", "value": row[1]} for row in result.all()]

    async def count_by_district(self) -> list:
        result = await self.db.execute(
            select(Crime.district, func.count(Crime.id))
            .group_by(Crime.district)
            .order_by(func.count(Crime.id).desc())
        )
        return [{"key": row[0] or "unknown", "value": row[1]} for row in result.all()]

    async def count_by_severity(self) -> list:
        result = await self.db.execute(
            select(Crime.severity, func.count(Crime.id))
            .group_by(Crime.severity)
            .order_by(func.count(Crime.id).desc())
        )
        return [{"key": row[0] or "unknown", "value": row[1]} for row in result.all()]
