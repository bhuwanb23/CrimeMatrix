from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.crime import Crime
from app.models.district import District
from app.models.crimetype import CrimeType
import structlog

logger = structlog.get_logger()


class CrimeCountEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def count_by_type(self) -> list:
        result = await self.db.execute(
            select(CrimeType.name, func.count(Crime.id))
            .join(CrimeType, Crime.crime_type_id == CrimeType.id, isouter=True)
            .group_by(CrimeType.name)
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
            select(District.name, func.count(Crime.id))
            .join(District, Crime.district_id == District.id, isouter=True)
            .group_by(District.name)
            .order_by(func.count(Crime.id).desc())
        )
        return [{"key": row[0] or "unknown", "value": row[1]} for row in result.all()]

    async def count_by_priority(self) -> list:
        result = await self.db.execute(
            select(Crime.priority, func.count(Crime.id))
            .group_by(Crime.priority)
            .order_by(func.count(Crime.id).desc())
        )
        return [{"key": row[0] or "unknown", "value": row[1]} for row in result.all()]
