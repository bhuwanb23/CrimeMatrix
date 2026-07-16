from app.repositories.base import BaseRepository
from app.models.case import Case
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


class CaseRepository(BaseRepository[Case]):
    def __init__(self, db: AsyncSession):
        super().__init__(Case, db)

    async def get_by_number(self, case_number: str):
        result = await self.db.execute(
            select(Case).where(Case.case_number == case_number)
        )
        return result.scalar_one_or_none()

    async def get_by_district(self, district: str) -> List[Case]:
        result = await self.db.execute(
            select(Case).where(Case.district == district)
        )
        return result.scalars().all()

    async def get_by_status(self, status: str) -> List[Case]:
        result = await self.db.execute(
            select(Case).where(Case.status == status)
        )
        return result.scalars().all()

    async def search(self, query: str) -> List[Case]:
        result = await self.db.execute(
            select(Case).where(
                Case.title.ilike(f"%{query}%") |
                Case.case_number.ilike(f"%{query}%") |
                Case.description.ilike(f"%{query}%")
            )
        )
        return result.scalars().all()
