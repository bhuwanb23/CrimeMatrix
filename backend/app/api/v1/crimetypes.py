from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.crimetype_repo import CrimeTypeRepository
from app.services.crimetype_service import CrimeTypeService
from app.schemas.crimetype import CrimeTypeCreate, CrimeTypeResponse
from app.schemas.common import PaginatedResponse, PaginationParams
from app.core.response import success_response
from app.db.phase1_store import store_create, store_get, store_list, using_phase1_store

router = APIRouter()


def get_service(db: AsyncSession):
    return CrimeTypeService(CrimeTypeRepository(db))


@router.get("/", )
async def list_crime_types(page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        data = await store_list("crime_types", page=page, page_size=page_size)
        data["items"] = [
            {
                "id": i.get("id"),
                "title": i.get("name") or "",
                "name": i.get("name"),
                "code": i.get("code"),
                "status": "active" if i.get("is_active", 1) else "inactive",
            }
            for i in data["items"]
        ]
        return {"success": True, "data": data, "message": "Success"}
    svc = get_service(db)
    params = PaginationParams(page=page, page_size=page_size)
    result = await svc.get_paginated(params); return {"success": True, "data": {"items": [{"id": i.id, "title": getattr(i, "title", getattr(i, "name", "")), "status": getattr(i, "status", "")} for i in result.items], "total": result.total, "page": result.page, "page_size": result.page_size, "total_pages": result.total_pages}, "message": "Success"}


@router.get("/{crimetype_id}")
async def get_crime_type(crimetype_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        ct = await store_get("crime_types", crimetype_id)
        if not ct:
            return success_response(message="Crime type not found")
        return success_response(data=ct)
    svc = get_service(db)
    ct = await svc.get_by_id(crimetype_id)
    if not ct:
        return success_response(message="Crime type not found")
    return success_response(data=CrimeTypeResponse.model_validate(ct).model_dump())


@router.post("/")
async def create_crime_type(data: CrimeTypeCreate, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        payload = data.model_dump()
        payload.setdefault("is_active", 1)
        try:
            ct = await store_create("crime_types", payload)
            return success_response(data=ct, message="Crime type created")
        except Exception as e:
            return success_response(message=str(e)[:200])
    svc = get_service(db)
    ct = await svc.create(data.model_dump())
    return success_response(data=CrimeTypeResponse.model_validate(ct).model_dump(), message="Crime type created")


@router.delete("/{crimetype_id}")
async def delete_crime_type(crimetype_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.delete(crimetype_id)
    return success_response(message="Crime type deleted" if deleted else "Crime type not found")

