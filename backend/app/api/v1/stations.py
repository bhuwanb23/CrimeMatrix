from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.station_repo import StationRepository
from app.services.station_service import StationService
from app.schemas.station import StationCreate, StationResponse
from app.schemas.common import PaginatedResponse, PaginationParams
from app.core.response import success_response
from app.db.phase1_store import store_get, store_list, using_phase1_store

router = APIRouter()


def get_service(db: AsyncSession):
    return StationService(StationRepository(db))


@router.get("/", )
async def list_stations(page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        data = await store_list("stations", page=page, page_size=page_size)
        data["items"] = [
            {
                "id": i.get("id"),
                "title": i.get("name") or "",
                "name": i.get("name"),
                "code": i.get("code"),
                "status": "active" if i.get("active", True) else "inactive",
            }
            for i in data["items"]
        ]
        return {"success": True, "data": data, "message": "Success"}
    svc = get_service(db)
    params = PaginationParams(page=page, page_size=page_size)
    result = await svc.get_paginated(params); return {"success": True, "data": {"items": [{"id": i.id, "title": getattr(i, "title", getattr(i, "name", "")), "status": getattr(i, "status", "")} for i in result.items], "total": result.total, "page": result.page, "page_size": result.page_size, "total_pages": result.total_pages}, "message": "Success"}


@router.get("/{station_id}")
async def get_station(station_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        station = await store_get("stations", station_id)
        if not station:
            return success_response(message="Station not found")
        return success_response(data=station)
    svc = get_service(db)
    station = await svc.get_by_id(station_id)
    if not station:
        return success_response(message="Station not found")
    return success_response(data=StationResponse.model_validate(station).model_dump())


@router.post("/")
async def create_station(data: StationCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    station = await svc.create(data.model_dump())
    return success_response(data=StationResponse.model_validate(station).model_dump(), message="Station created")


@router.delete("/{station_id}")
async def delete_station(station_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.delete(station_id)
    return success_response(message="Station deleted" if deleted else "Station not found")

