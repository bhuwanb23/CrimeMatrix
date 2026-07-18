from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.search import SavedSearch
from app.core.response import success_response

router = APIRouter()


class SavedSearchCreate(BaseModel):
    user_id: str = "default"
    name: str
    query: str
    filters: Optional[str] = None


@router.get("")
async def list_saved_searches(user_id: str = "default", db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(SavedSearch).where(SavedSearch.user_id == int(user_id) if user_id.isdigit() else True)
        .order_by(SavedSearch.created_at.desc())
    )
    searches = [
        {"id": s.id, "name": s.name, "query": s.query, "filters": s.filters, "created_at": str(s.created_at) if s.created_at else None}
        for s in result.scalars().all()
    ]
    return success_response(data=searches)


@router.post("")
async def create_saved_search(data: SavedSearchCreate, db: AsyncSession = Depends(get_db)):
    ss = SavedSearch(
        user_id=0,
        name=data.name,
        query=data.query,
        filters=data.filters,
    )
    db.add(ss)
    await db.commit()
    return success_response(data={"id": ss.id, "name": ss.name})


@router.delete("/{search_id}")
async def delete_saved_search(search_id: int, db: AsyncSession = Depends(get_db)):
    await db.execute(delete(SavedSearch).where(SavedSearch.id == search_id))
    await db.commit()
    return success_response(message="Deleted")
