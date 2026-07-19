from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.bookmark_service import BookmarkService
from pydantic import BaseModel
from typing import Optional
from app.core.response import success_response

router = APIRouter()


class BookmarkToggleRequest(BaseModel):
    user_id: int = 1
    entity_type: str
    entity_id: int
    bookmark_note: Optional[str] = None


class BookmarkCreateRequest(BaseModel):
    user_id: int = 1
    entity_type: str
    entity_id: int
    bookmark_note: Optional[str] = None
    investigation_id: Optional[int] = None


class BookmarkNoteUpdate(BaseModel):
    bookmark_note: str


def get_service(db: AsyncSession):
    return BookmarkService(db)


@router.get("/")
async def list_bookmarks(
    user_id: int = Query(default=1),
    entity_type: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    bookmarks = await svc.list_bookmarks(user_id, entity_type)
    return success_response(data={"items": bookmarks, "total": len(bookmarks)})


@router.get("/grouped")
async def get_grouped_bookmarks(
    user_id: int = Query(default=1),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    grouped = await svc.get_bookmarks_grouped(user_id)
    return success_response(data=grouped)


@router.get("/check")
async def check_bookmark(
    user_id: int = Query(default=1),
    entity_type: str = Query(...),
    entity_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.is_bookmarked(user_id, entity_type, entity_id)
    return success_response(data={"bookmarked": result is not None, "bookmark": result})


@router.get("/count")
async def bookmark_count(
    entity_type: str = Query(...),
    entity_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    count = await svc.get_bookmark_count(entity_type, entity_id)
    return success_response(data={"count": count})


@router.post("/")
async def create_bookmark(data: BookmarkCreateRequest, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.create_bookmark(
        user_id=data.user_id,
        entity_type=data.entity_type,
        entity_id=data.entity_id,
        bookmark_note=data.bookmark_note,
        investigation_id=data.investigation_id,
    )
    if result.get("already_exists"):
        return success_response(data=result, message="Already bookmarked")
    return success_response(data=result, message="Bookmark created")


@router.post("/toggle")
async def toggle_bookmark(data: BookmarkToggleRequest, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.toggle_bookmark(
        user_id=data.user_id,
        entity_type=data.entity_type,
        entity_id=data.entity_id,
        bookmark_note=data.bookmark_note,
    )
    action = "added" if result["bookmarked"] else "removed"
    return success_response(data=result, message=f"Bookmark {action}")


@router.put("/{bookmark_id}/note")
async def update_bookmark_note(bookmark_id: int, data: BookmarkNoteUpdate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.update_note(bookmark_id, data.bookmark_note)
    if not result:
        return success_response(message="Bookmark not found")
    return success_response(data=result, message="Note updated")


@router.delete("/{bookmark_id}")
async def delete_bookmark(bookmark_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.remove_bookmark_by_id(bookmark_id)
    return success_response(message="Bookmark deleted" if deleted else "Bookmark not found")


@router.delete("/")
async def remove_bookmark(
    user_id: int = Query(default=1),
    entity_type: str = Query(...),
    entity_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    removed = await svc.remove_bookmark(user_id, entity_type, entity_id)
    return success_response(message="Bookmark removed" if removed else "Bookmark not found")
