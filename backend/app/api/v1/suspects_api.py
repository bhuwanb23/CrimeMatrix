from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.session import get_db
from app.models.suspect import Suspect
from app.core.response import success_response

router = APIRouter()


@router.get("/")
async def list_suspects(
    page: int = 1,
    page_size: int = 20,
    search: str = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Suspect)
    if search:
        stmt = stmt.where(Suspect.name.ilike(f"%{search}%"))

    # Get total count
    count_stmt = select(func.count(Suspect.id))
    if search:
        count_stmt = count_stmt.where(Suspect.name.ilike(f"%{search}%"))
    total = (await db.execute(count_stmt)).scalar() or 0

    # Paginate
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    suspects = result.scalars().all()

    items = []
    for s in suspects:
        items.append({
            "id": s.id,
            "name": s.name,
            "alias": s.name,
            "age": s.age,
            "gender": s.gender,
            "district": s.district,
            "status": s.status,
            "risk_score": s.risk_score or 0,
            "description": s.description,
        })

    return success_response(data={
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    })


@router.get("/{suspect_id}")
async def get_suspect(suspect_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Suspect).where(Suspect.id == suspect_id)
    result = await db.execute(stmt)
    suspect = result.scalar()
    if not suspect:
        return success_response(message="Suspect not found")
    return success_response(data={
        "id": suspect.id,
        "name": suspect.name,
        "age": suspect.age,
        "gender": suspect.gender,
        "district": suspect.district,
        "status": suspect.status,
        "risk_score": suspect.risk_score or 0,
        "description": suspect.description,
        "physical_description": suspect.physical_description,
    })
