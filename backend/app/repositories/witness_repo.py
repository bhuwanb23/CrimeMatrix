from app.repositories.base import BaseRepository
from app.models.witness import Witness
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


class WitnessRepository(BaseRepository[Witness]):
    def __init__(self, db: AsyncSession):
        super().__init__(Witness, db)
