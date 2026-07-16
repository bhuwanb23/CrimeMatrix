from app.repositories.base import BaseRepository
from app.models.case_status_log import CaseStatusLog
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List


class CaseStatusRepository(BaseRepository[CaseStatusLog]):
    def __init__(self, db: AsyncSession):
        super().__init__(CaseStatusLog, db)

    async def get_by_investigation(self, investigation_id: int) -> List[CaseStatusLog]:
        result = await self.db.execute(
            select(CaseStatusLog).where(CaseStatusLog.investigation_id == investigation_id)
        )
        return result.scalars().all()
