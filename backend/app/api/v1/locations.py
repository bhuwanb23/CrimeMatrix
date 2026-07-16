from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.location_repo import LocationRepository
from app.services.location_service import LocationService
from app.schemas.location import LocationCreate, LocationResponse
from app.schemas.common import PaginatedResponse, PaginationParams
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return LocationService(LocationRepository(db))


@router.get("/", response_model=PaginatedResponse)
async def list_locations(page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    params = PaginationParams(page=page, page_size=page_size)
    return success_response(data=(await svc.get_paginated(params)).model_dump())


@router.get("/{location_id}")
async def get_location(location_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    location = await svc.get_by_id(location_id)
    if not location:
        return success_response(message="Location not found")
    return success_response(data=LocationResponse.model_validate(location).model_dump())


@router.post("/")
async def create_location(data: LocationCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    location = await svc.create(data.model_dump())
    return success_response(data=LocationResponse.model_validate(location).model_dump(), message="Location created")


@router.delete("/{location_id}")
async def delete_location(location_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.delete(location_id)
    return success_response(message="Location deleted" if deleted else "Location not found")
