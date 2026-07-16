from app.repositories.base import BaseRepository
from app.models.note import Note
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List


class NoteRepository(BaseRepository[Note]):
    def __init__(self, db: AsyncSession):
        super().__init__(Note, db)

    async def get_by_investigation(self, investigation_id: int) -> List[Note]:
        result = await self.db.execute(
            select(Note).where(Note.investigation_id == investigation_id)
        )
        return result.scalars().all()
