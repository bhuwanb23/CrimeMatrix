from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.victim_repo import VictimRepository
from app.services.victim_service import VictimService
from app.schemas.victim import VictimCreate, VictimResponse
from app.schemas.common import PaginatedResponse, PaginationParams
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return VictimService(VictimRepository(db))


@router.get("/", )
async def list_victims(page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    params = PaginationParams(page=page, page_size=page_size)
    result = await svc.get_paginated(params); return {"success": True, "data": {"items": [{"id": i.id, "title": getattr(i, "title", getattr(i, "name", "")), "status": getattr(i, "status", "")} for i in result.items], "total": result.total, "page": result.page, "page_size": result.page_size, "total_pages": result.total_pages}, "message": "Success"}


@router.get("/{victim_id}")
async def get_victim(victim_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    victim = await svc.get_by_id(victim_id)
    if not victim:
        return success_response(message="Victim not found")
    return success_response(data=VictimResponse.model_validate(victim).model_dump())


@router.post("/")
async def create_victim(data: VictimCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    victim = await svc.create(data.model_dump())
    return success_response(data=VictimResponse.model_validate(victim).model_dump(), message="Victim created")


@router.delete("/{victim_id}")
async def delete_victim(victim_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.delete(victim_id)
    return success_response(message="Victim deleted" if deleted else "Victim not found")

