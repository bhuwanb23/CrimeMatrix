from app.repositories.base import BaseRepository
from app.models.station import Station
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


class StationRepository(BaseRepository[Station]):
    def __init__(self, db: AsyncSession):
        super().__init__(Station, db)
