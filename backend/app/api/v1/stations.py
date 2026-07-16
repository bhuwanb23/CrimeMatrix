from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.station_repo import StationRepository
from app.services.station_service import StationService
from app.schemas.station import StationCreate, StationResponse
from app.schemas.common import PaginatedResponse, PaginationParams
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return StationService(StationRepository(db))


@router.get("/", response_model=PaginatedResponse)
async def list_stations(page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    params = PaginationParams(page=page, page_size=page_size)
    return success_response(data=(await svc.get_paginated(params)).model_dump())


@router.get("/{station_id}")
async def get_station(station_id: int, db: AsyncSession = Depends(get_db)):
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
