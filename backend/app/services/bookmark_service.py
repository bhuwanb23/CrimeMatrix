from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.bookmark import Bookmark
import structlog

logger = structlog.get_logger()


class BookmarkService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_bookmarks(self, user_id: int, entity_type: str = None) -> List[dict]:
        stmt = select(Bookmark).where(Bookmark.user_id == user_id)
        if entity_type:
            stmt = stmt.where(Bookmark.entity_type == entity_type)
        stmt = stmt.order_by(Bookmark.created_at.desc())
        result = await self.db.execute(stmt)
        bookmarks = result.scalars().all()
        return [self._to_dict(b) for b in bookmarks]

    async def create_bookmark(self, user_id: int, entity_type: str, entity_id: int,
                               bookmark_note: str = None, investigation_id: int = None) -> dict:
        existing = await self.is_bookmarked(user_id, entity_type, entity_id)
        if existing:
            return {"id": existing["id"], "already_exists": True}

        bookmark = Bookmark(
            user_id=user_id,
            entity_type=entity_type,
            entity_id=entity_id,
            bookmark_note=bookmark_note,
            investigation_id=investigation_id,
        )
        self.db.add(bookmark)
        await self.db.commit()
        await self.db.refresh(bookmark)
        return {**self._to_dict(bookmark), "already_exists": False}

    async def remove_bookmark(self, user_id: int, entity_type: str, entity_id: int) -> bool:
        stmt = select(Bookmark).where(
            Bookmark.user_id == user_id,
            Bookmark.entity_type == entity_type,
            Bookmark.entity_id == entity_id,
        )
        result = await self.db.execute(stmt)
        bookmark = result.scalar()
        if not bookmark:
            return False
        await self.db.delete(bookmark)
        await self.db.commit()
        return True

    async def remove_bookmark_by_id(self, bookmark_id: int) -> bool:
        stmt = select(Bookmark).where(Bookmark.id == bookmark_id)
        result = await self.db.execute(stmt)
        bookmark = result.scalar()
        if not bookmark:
            return False
        await self.db.delete(bookmark)
        await self.db.commit()
        return True

    async def is_bookmarked(self, user_id: int, entity_type: str, entity_id: int) -> Optional[dict]:
        stmt = select(Bookmark).where(
            Bookmark.user_id == user_id,
            Bookmark.entity_type == entity_type,
            Bookmark.entity_id == entity_id,
        )
        result = await self.db.execute(stmt)
        bookmark = result.scalar()
        return self._to_dict(bookmark) if bookmark else None

    async def toggle_bookmark(self, user_id: int, entity_type: str, entity_id: int,
                               bookmark_note: str = None) -> dict:
        existing = await self.is_bookmarked(user_id, entity_type, entity_id)
        if existing:
            await self.remove_bookmark(user_id, entity_type, entity_id)
            return {"bookmarked": False, "bookmark_id": None}
        else:
            result = await self.create_bookmark(user_id, entity_type, entity_id, bookmark_note)
            return {"bookmarked": True, "bookmark_id": result.get("id")}

    async def get_bookmark_count(self, entity_type: str, entity_id: int) -> int:
        stmt = select(sql_func.count(Bookmark.id)).where(
            Bookmark.entity_type == entity_type,
            Bookmark.entity_id == entity_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_bookmarks_grouped(self, user_id: int) -> dict:
        bookmarks = await self.list_bookmarks(user_id)
        grouped = {}
        for b in bookmarks:
            etype = b["entity_type"]
            if etype not in grouped:
                grouped[etype] = []
            grouped[etype].append(b)
        return grouped

    async def update_note(self, bookmark_id: int, note: str) -> Optional[dict]:
        stmt = select(Bookmark).where(Bookmark.id == bookmark_id)
        result = await self.db.execute(stmt)
        bookmark = result.scalar()
        if not bookmark:
            return None
        bookmark.bookmark_note = note
        await self.db.commit()
        await self.db.refresh(bookmark)
        return self._to_dict(bookmark)

    def _to_dict(self, bookmark: Bookmark) -> dict:
        return {
            "id": bookmark.id,
            "user_id": bookmark.user_id,
            "entity_type": bookmark.entity_type,
            "entity_id": bookmark.entity_id,
            "bookmark_note": bookmark.bookmark_note,
            "investigation_id": bookmark.investigation_id,
            "created_at": str(bookmark.created_at) if bookmark.created_at else None,
        }
