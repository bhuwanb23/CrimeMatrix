from app.repositories.base import BaseRepository
from app.models.district import District
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


class DistrictRepository(BaseRepository[District]):
    def __init__(self, db: AsyncSession):
        super().__init__(District, db)
