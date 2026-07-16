from app.repositories.base import BaseRepository
from app.models.criminal import Criminal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List


class CriminalRepository(BaseRepository[Criminal]):
    def __init__(self, db: AsyncSession):
        super().__init__(Criminal, db)

    async def get_by_status(self, status: str) -> List[Criminal]:
        result = await self.db.execute(select(Criminal).where(Criminal.status == status))
        return result.scalars().all()

    async def get_high_risk(self, min_score: float = 70.0) -> List[Criminal]:
        result = await self.db.execute(select(Criminal).where(Criminal.risk_score >= min_score))
        return result.scalars().all()
