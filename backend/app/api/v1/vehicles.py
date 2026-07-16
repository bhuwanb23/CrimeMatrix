from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.vehicle_repo import VehicleRepository
from app.services.vehicle_service import VehicleService
from app.schemas.vehicle import VehicleCreate, VehicleResponse
from app.schemas.common import PaginatedResponse, PaginationParams
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return VehicleService(VehicleRepository(db))


@router.get("/", response_model=PaginatedResponse)
async def list_vehicles(page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    params = PaginationParams(page=page, page_size=page_size)
    return success_response(data=(await svc.get_paginated(params)).model_dump())


@router.get("/{vehicle_id}")
async def get_vehicle(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    vehicle = await svc.get_by_id(vehicle_id)
    if not vehicle:
        return success_response(message="Vehicle not found")
    return success_response(data=VehicleResponse.model_validate(vehicle).model_dump())


@router.post("/")
async def create_vehicle(data: VehicleCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    vehicle = await svc.create(data.model_dump())
    return success_response(data=VehicleResponse.model_validate(vehicle).model_dump(), message="Vehicle created")


@router.delete("/{vehicle_id}")
async def delete_vehicle(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.delete(vehicle_id)
    return success_response(message="Vehicle deleted" if deleted else "Vehicle not found")


@router.get("/registration/{reg}")
async def get_by_registration(reg: str, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    vehicle = await svc.get_by_registration(reg)
    if not vehicle:
        return success_response(message="Vehicle not found")
    return success_response(data=VehicleResponse.model_validate(vehicle).model_dump())
