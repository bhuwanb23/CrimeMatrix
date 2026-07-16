from app.repositories.base import BaseRepository
from app.models.victim import Victim
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


class VictimRepository(BaseRepository[Victim]):
    def __init__(self, db: AsyncSession):
        super().__init__(Victim, db)
