from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.vehicle_repo import VehicleRepository
from app.services.vehicle_service import VehicleService
from app.schemas.vehicle import VehicleCreate, VehicleResponse
from app.schemas.common import PaginatedResponse, PaginationParams
from app.core.response import success_response
from app.db.phase1_store import store_create, store_get, store_list, using_phase1_store

router = APIRouter()


def get_service(db: AsyncSession):
    return VehicleService(VehicleRepository(db))


@router.get("/", )
async def list_vehicles(page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        data = await store_list("vehicles", page=page, page_size=page_size)
        data["items"] = [
            {
                "id": i.get("id"),
                "title": i.get("registration_number") or "",
                "registration_number": i.get("registration_number"),
                "status": i.get("status"),
            }
            for i in data["items"]
        ]
        return {"success": True, "data": data, "message": "Success"}
    svc = get_service(db)
    params = PaginationParams(page=page, page_size=page_size)
    result = await svc.get_paginated(params); return {"success": True, "data": {"items": [{"id": i.id, "title": getattr(i, "title", getattr(i, "name", "")), "status": getattr(i, "status", "")} for i in result.items], "total": result.total, "page": result.page, "page_size": result.page_size, "total_pages": result.total_pages}, "message": "Success"}


@router.get("/{vehicle_id}")
async def get_vehicle(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        vehicle = await store_get("vehicles", vehicle_id)
        if not vehicle:
            return success_response(message="Vehicle not found")
        return success_response(data=vehicle)
    svc = get_service(db)
    vehicle = await svc.get_by_id(vehicle_id)
    if not vehicle:
        return success_response(message="Vehicle not found")
    return success_response(data=VehicleResponse.model_validate(vehicle).model_dump())


@router.post("/")
async def create_vehicle(data: VehicleCreate, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        payload = data.model_dump()
        payload.setdefault("status", "active")
        try:
            vehicle = await store_create("vehicles", payload)
            return success_response(data=vehicle, message="Vehicle created")
        except Exception as e:
            return success_response(message=str(e)[:200])
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

