from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.district_repo import DistrictRepository
from app.services.district_service import DistrictService
from app.schemas.district import DistrictCreate, DistrictResponse
from app.schemas.common import PaginatedResponse, PaginationParams
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return DistrictService(DistrictRepository(db))


@router.get("/", )
async def list_districts(page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    params = PaginationParams(page=page, page_size=page_size)
    result = await svc.get_paginated(params); return {"success": True, "data": {"items": [{"id": i.id, "title": getattr(i, "title", getattr(i, "name", "")), "status": getattr(i, "status", "")} for i in result.items], "total": result.total, "page": result.page, "page_size": result.page_size, "total_pages": result.total_pages}, "message": "Success"}


@router.get("/{district_id}")
async def get_district(district_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    district = await svc.get_by_id(district_id)
    if not district:
        return success_response(message="District not found")
    return success_response(data=DistrictResponse.model_validate(district).model_dump())


@router.post("/")
async def create_district(data: DistrictCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    district = await svc.create(data.model_dump())
    return success_response(data=DistrictResponse.model_validate(district).model_dump(), message="District created")


@router.delete("/{district_id}")
async def delete_district(district_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.delete(district_id)
    return success_response(message="District deleted" if deleted else "District not found")

