from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.session import get_db
from app.models.suspect import Suspect
from app.core.response import success_response
from app.db.phase1_store import store_get, store_list, using_phase1_store

router = APIRouter()


@router.get("/")
async def list_suspects(
    page: int = 1,
    page_size: int = 20,
    search: str = None,
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        data = await store_list("suspects", page=page, page_size=page_size)
        items = data["items"]
        if search:
            q = search.lower()
            items = [s for s in items if q in str(s.get("name", "")).lower()]
        return success_response(
            data={
                "items": [
                    {
                        "id": s.get("id"),
                        "name": s.get("name"),
                        "alias": s.get("name"),
                        "age": s.get("age"),
                        "district": s.get("district"),
                        "status": s.get("status"),
                        "risk_score": s.get("risk_score") or 0,
                    }
                    for s in items
                ],
                "total": len(items) if search else data.get("total", len(items)),
                "page": page,
                "page_size": page_size,
                "total_pages": data.get("total_pages", 1),
            }
        )
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
    if using_phase1_store():
        suspect = await store_get("suspects", suspect_id)
        if not suspect:
            return success_response(message="Suspect not found")
        return success_response(
            data={
                "id": suspect.get("id"),
                "name": suspect.get("name"),
                "age": suspect.get("age"),
                "district": suspect.get("district"),
                "status": suspect.get("status"),
                "risk_score": suspect.get("risk_score") or 0,
                "description": suspect.get("description"),
            }
        )
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
