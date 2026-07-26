from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.criminal_repo import CriminalRepository
from app.services.criminal_service import CriminalService
from app.schemas.criminal import CriminalCreate, CriminalResponse
from app.schemas.common import PaginatedResponse, PaginationParams
from app.core.response import success_response
from app.db.phase1_store import store_get, store_list, using_phase1_store

router = APIRouter()


def get_service(db: AsyncSession):
    return CriminalService(CriminalRepository(db))


@router.get("/", )
async def list_criminals(page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        data = await store_list("criminals", page=page, page_size=page_size)
        data["items"] = [
            {
                "id": i.get("id"),
                "title": i.get("alias") or f"Criminal {i.get('id')}",
                "name": i.get("alias"),
                "status": i.get("status"),
                "risk_score": i.get("risk_score"),
            }
            for i in data["items"]
        ]
        return {"success": True, "data": data, "message": "Success"}
    svc = get_service(db)
    params = PaginationParams(page=page, page_size=page_size)
    result = await svc.get_paginated(params); return {"success": True, "data": {"items": [{"id": i.id, "title": getattr(i, "title", getattr(i, "name", "")), "status": getattr(i, "status", "")} for i in result.items], "total": result.total, "page": result.page, "page_size": result.page_size, "total_pages": result.total_pages}, "message": "Success"}


@router.get("/high-risk")
async def high_risk_criminals(min_score: float = 70.0, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        data = await store_list("criminals", page=1, page_size=100)
        items = [i for i in data["items"] if float(i.get("risk_score") or 0) >= min_score]
        return success_response(data=items)
    svc = get_service(db)
    results = await svc.get_high_risk(min_score)
    return success_response(data=[CriminalResponse.model_validate(r).model_dump() for r in results])


@router.get("/{criminal_id}")
async def get_criminal(criminal_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        criminal = await store_get("criminals", criminal_id)
        if not criminal:
            return success_response(message="Criminal not found")
        return success_response(data=criminal)
    svc = get_service(db)
    criminal = await svc.get_by_id(criminal_id)
    if not criminal:
        return success_response(message="Criminal not found")
    return success_response(data=CriminalResponse.model_validate(criminal).model_dump())


@router.post("/")
async def create_criminal(data: CriminalCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    criminal = await svc.create(data.model_dump())
    return success_response(data=CriminalResponse.model_validate(criminal).model_dump(), message="Criminal created")


@router.put("/{criminal_id}")
async def update_criminal(criminal_id: int, data: CriminalCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    criminal = await svc.update(criminal_id, data.model_dump(exclude_unset=True))
    if not criminal:
        return success_response(message="Criminal not found")
    return success_response(data=CriminalResponse.model_validate(criminal).model_dump(), message="Criminal updated")


@router.delete("/{criminal_id}")
async def delete_criminal(criminal_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.delete(criminal_id)
    return success_response(message="Criminal deleted" if deleted else "Criminal not found")

