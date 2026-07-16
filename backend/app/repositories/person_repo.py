from app.repositories.base import BaseRepository
from app.models.person import Person
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List


class PersonRepository(BaseRepository[Person]):
    def __init__(self, db: AsyncSession):
        super().__init__(Person, db)

    async def search(self, query: str) -> List[Person]:
        result = await self.db.execute(
            select(Person).where(
                Person.first_name.ilike(f"%{query}%") |
                Person.last_name.ilike(f"%{query}%")
            )
        )
        return result.scalars().all()
