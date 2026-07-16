from app.repositories.base import BaseRepository
from app.models.case_link import CaseLink
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List


class CaseLinkRepository(BaseRepository[CaseLink]):
    def __init__(self, db: AsyncSession):
        super().__init__(CaseLink, db)

    async def get_by_investigation(self, investigation_id: int) -> List[CaseLink]:
        result = await self.db.execute(
            select(CaseLink).where(CaseLink.investigation_id == investigation_id)
        )
        return result.scalars().all()
