from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.officer_repo import OfficerRepository
from app.services.officer_service import OfficerService
from app.schemas.officer import OfficerCreate, OfficerResponse
from app.schemas.common import PaginatedResponse, PaginationParams
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return OfficerService(OfficerRepository(db))


@router.get("/", )
async def list_officers(page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    params = PaginationParams(page=page, page_size=page_size)
    result = await svc.get_paginated(params); return {"success": True, "data": {"items": [{"id": i.id, "title": getattr(i, "title", getattr(i, "name", "")), "status": getattr(i, "status", "")} for i in result.items], "total": result.total, "page": result.page, "page_size": result.page_size, "total_pages": result.total_pages}, "message": "Success"}


@router.get("/{officer_id}")
async def get_officer(officer_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    officer = await svc.get_by_id(officer_id)
    if not officer:
        return success_response(message="Officer not found")
    return success_response(data=OfficerResponse.model_validate(officer).model_dump())


@router.post("/")
async def create_officer(data: OfficerCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    officer = await svc.create(data.model_dump())
    return success_response(data=OfficerResponse.model_validate(officer).model_dump(), message="Officer created")


@router.delete("/{officer_id}")
async def delete_officer(officer_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.delete(officer_id)
    return success_response(message="Officer deleted" if deleted else "Officer not found")


@router.get("/station/{station_id}")
async def officers_by_station(station_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    results = await svc.get_by_station(station_id)
    return success_response(data=[OfficerResponse.model_validate(r).model_dump() for r in results])

