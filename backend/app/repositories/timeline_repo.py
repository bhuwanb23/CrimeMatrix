from app.repositories.base import BaseRepository
from app.models.timeline_event import TimelineEvent
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List


class TimelineRepository(BaseRepository[TimelineEvent]):
    def __init__(self, db: AsyncSession):
        super().__init__(TimelineEvent, db)

    async def get_by_investigation(self, investigation_id: int) -> List[TimelineEvent]:
        result = await self.db.execute(
            select(TimelineEvent).where(TimelineEvent.investigation_id == investigation_id)
        )
        return result.scalars().all()
