from app.repositories.base import BaseRepository
from app.models.bookmark import Bookmark
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List


class BookmarkRepository(BaseRepository[Bookmark]):
    def __init__(self, db: AsyncSession):
        super().__init__(Bookmark, db)

    async def get_by_user(self, user_id: int) -> List[Bookmark]:
        result = await self.db.execute(
            select(Bookmark).where(Bookmark.user_id == user_id)
        )
        return result.scalars().all()

    async def is_bookmarked(self, user_id: int, investigation_id: int) -> bool:
        result = await self.db.execute(
            select(Bookmark).where(
                Bookmark.user_id == user_id,
                Bookmark.investigation_id == investigation_id,
            )
        )
        return result.scalar_one_or_none() is not None
