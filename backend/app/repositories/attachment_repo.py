from app.repositories.base import BaseRepository
from app.models.attachment import Attachment
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List


class AttachmentRepository(BaseRepository[Attachment]):
    def __init__(self, db: AsyncSession):
        super().__init__(Attachment, db)

    async def get_by_investigation(self, investigation_id: int) -> List[Attachment]:
        result = await self.db.execute(
            select(Attachment).where(Attachment.investigation_id == investigation_id)
        )
        return result.scalars().all()
