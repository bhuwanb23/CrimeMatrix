from app.repositories.base import BaseRepository
from app.models.case import Case
from sqlalchemy import select, or_
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

    async def get_by_crime_no(self, crime_no: str):
        result = await self.db.execute(
            select(Case).where(Case.crime_no == crime_no)
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

    async def get_by_category(self, case_category_id: int) -> List[Case]:
        result = await self.db.execute(
            select(Case).where(Case.case_category_id == case_category_id)
        )
        return result.scalars().all()

    async def get_by_station(self, police_station_id: int) -> List[Case]:
        result = await self.db.execute(
            select(Case).where(Case.police_station_id == police_station_id)
        )
        return result.scalars().all()

    async def search(self, query: str) -> List[Case]:
        result = await self.db.execute(
            select(Case).where(
                Case.title.ilike(f"%{query}%") |
                Case.case_number.ilike(f"%{query}%") |
                Case.crime_no.ilike(f"%{query}%") |
                Case.description.ilike(f"%{query}%") |
                Case.crime_type.ilike(f"%{query}%") |
                Case.district.ilike(f"%{query}%")
            )
        )
        return result.scalars().all()
