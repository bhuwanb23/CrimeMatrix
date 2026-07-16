from app.repositories.base import BaseRepository
from app.models.suspect import Suspect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


class SuspectRepository(BaseRepository[Suspect]):
    def __init__(self, db: AsyncSession):
        super().__init__(Suspect, db)

    async def get_by_status(self, status: str) -> List[Suspect]:
        result = await self.db.execute(
            select(Suspect).where(Suspect.status == status)
        )
        return result.scalars().all()

    async def get_high_risk(self, min_score: float = 70.0) -> List[Suspect]:
        result = await self.db.execute(
            select(Suspect).where(Suspect.risk_score >= min_score)
        )
        return result.scalars().all()

    async def search(self, query: str) -> List[Suspect]:
        result = await self.db.execute(
            select(Suspect).where(
                Suspect.name.ilike(f"%{query}%") |
                Suspect.district.ilike(f"%{query}%")
            )
        )
        return result.scalars().all()
