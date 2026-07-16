from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.bookmark_repo import BookmarkRepository
from app.schemas.bookmark import BookmarkCreate, BookmarkResponse
from app.core.response import success_response

router = APIRouter()


@router.get("/user/{user_id}")
async def list_bookmarks(user_id: int, db: AsyncSession = Depends(get_db)):
    repo = BookmarkRepository(db)
    bookmarks = await repo.get_by_user(user_id)
    return success_response(data=[BookmarkResponse.model_validate(b).model_dump() for b in bookmarks])


@router.post("/")
async def create_bookmark(data: BookmarkCreate, db: AsyncSession = Depends(get_db)):
    repo = BookmarkRepository(db)
    existing = await repo.is_bookmarked(data.user_id, data.investigation_id)
    if existing:
        return success_response(message="Already bookmarked")
    bookmark = await repo.create(data.model_dump())
    return success_response(data=BookmarkResponse.model_validate(bookmark).model_dump(), message="Bookmark created")


@router.delete("/{bookmark_id}")
async def delete_bookmark(bookmark_id: int, db: AsyncSession = Depends(get_db)):
    repo = BookmarkRepository(db)
    deleted = await repo.delete(bookmark_id)
    return success_response(message="Bookmark deleted" if deleted else "Bookmark not found")
