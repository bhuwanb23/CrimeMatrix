from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.search import SearchHistory
from app.core.response import success_response

router = APIRouter()


class SearchHistoryCreate(BaseModel):
    user_id: str = "default"
    query: str
    results_count: int = 0


@router.get("")
async def list_search_history(user_id: str = "default", db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(SearchHistory).where(SearchHistory.user_id == int(user_id) if user_id.isdigit() else True)
        .order_by(SearchHistory.created_at.desc()).limit(50)
    )
    history = [
        {"id": h.id, "query": h.query, "results_count": h.results_count, "created_at": str(h.created_at) if h.created_at else None}
        for h in result.scalars().all()
    ]
    return success_response(data=history)


@router.post("")
async def record_search(data: SearchHistoryCreate, db: AsyncSession = Depends(get_db)):
    sh = SearchHistory(
        user_id=int(data.user_id) if data.user_id.isdigit() else None,
        query=data.query,
        results_count=data.results_count,
    )
    db.add(sh)
    await db.commit()
    return success_response(data={"id": sh.id})


@router.delete("")
async def clear_search_history(user_id: str = "default", db: AsyncSession = Depends(get_db)):
    await db.execute(delete(SearchHistory))
    await db.commit()
    return success_response(message="History cleared")
