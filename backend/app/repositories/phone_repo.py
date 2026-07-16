from app.repositories.base import BaseRepository
from app.models.phone import Phone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List


class PhoneRepository(BaseRepository[Phone]):
    def __init__(self, db: AsyncSession):
        super().__init__(Phone, db)

    async def get_by_number(self, number: str) -> Phone:
        result = await self.db.execute(select(Phone).where(Phone.number == number))
        return result.scalar_one_or_none()
