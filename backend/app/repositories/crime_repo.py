from app.repositories.base import BaseRepository
from app.models.crime import Crime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List


class CrimeRepository(BaseRepository[Crime]):
    def __init__(self, db: AsyncSession):
        super().__init__(Crime, db)

    async def get_by_district(self, district_id: int) -> List[Crime]:
        result = await self.db.execute(select(Crime).where(Crime.district_id == district_id))
        return result.scalars().all()

    async def get_by_status(self, status: str) -> List[Crime]:
        result = await self.db.execute(select(Crime).where(Crime.status == status))
        return result.scalars().all()

    async def search(self, query: str) -> List[Crime]:
        result = await self.db.execute(
            select(Crime).where(
                Crime.title.ilike(f"%{query}%") | Crime.description.ilike(f"%{query}%")
            )
        )
        return result.scalars().all()
