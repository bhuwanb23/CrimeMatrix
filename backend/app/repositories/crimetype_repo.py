from app.repositories.base import BaseRepository
from app.models.crimetype import CrimeType
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


class CrimeTypeRepository(BaseRepository[CrimeType]):
    def __init__(self, db: AsyncSession):
        super().__init__(CrimeType, db)
