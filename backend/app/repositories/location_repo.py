from app.repositories.base import BaseRepository
from app.models.location import Location
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


class LocationRepository(BaseRepository[Location]):
    def __init__(self, db: AsyncSession):
        super().__init__(Location, db)
