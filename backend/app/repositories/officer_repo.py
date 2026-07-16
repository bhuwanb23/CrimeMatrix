from app.repositories.base import BaseRepository
from app.models.officer import Officer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List


class OfficerRepository(BaseRepository[Officer]):
    def __init__(self, db: AsyncSession):
        super().__init__(Officer, db)

    async def get_by_station(self, station_id: int) -> List[Officer]:
        result = await self.db.execute(select(Officer).where(Officer.station_id == station_id))
        return result.scalars().all()
