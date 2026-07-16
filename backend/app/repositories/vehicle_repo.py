from app.repositories.base import BaseRepository
from app.models.vehicle import Vehicle
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List


class VehicleRepository(BaseRepository[Vehicle]):
    def __init__(self, db: AsyncSession):
        super().__init__(Vehicle, db)

    async def get_by_registration(self, reg: str) -> Vehicle:
        result = await self.db.execute(select(Vehicle).where(Vehicle.registration_number == reg))
        return result.scalar_one_or_none()
