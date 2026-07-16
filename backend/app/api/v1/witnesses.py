from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.witness_repo import WitnessRepository
from app.services.witness_service import WitnessService
from app.schemas.witness import WitnessCreate, WitnessResponse
from app.schemas.common import PaginatedResponse, PaginationParams
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return WitnessService(WitnessRepository(db))


@router.get("/", )
async def list_witnesses(page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    params = PaginationParams(page=page, page_size=page_size)
    result = await svc.get_paginated(params); return {"success": True, "data": {"items": [{"id": i.id, "title": getattr(i, "title", getattr(i, "name", "")), "status": getattr(i, "status", "")} for i in result.items], "total": result.total, "page": result.page, "page_size": result.page_size, "total_pages": result.total_pages}, "message": "Success"}


@router.get("/{witness_id}")
async def get_witness(witness_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    witness = await svc.get_by_id(witness_id)
    if not witness:
        return success_response(message="Witness not found")
    return success_response(data=WitnessResponse.model_validate(witness).model_dump())


@router.post("/")
async def create_witness(data: WitnessCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    witness = await svc.create(data.model_dump())
    return success_response(data=WitnessResponse.model_validate(witness).model_dump(), message="Witness created")


@router.delete("/{witness_id}")
async def delete_witness(witness_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.delete(witness_id)
    return success_response(message="Witness deleted" if deleted else "Witness not found")

