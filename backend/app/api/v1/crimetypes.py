from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.crimetype_repo import CrimeTypeRepository
from app.services.crimetype_service import CrimeTypeService
from app.schemas.crimetype import CrimeTypeCreate, CrimeTypeResponse
from app.schemas.common import PaginatedResponse, PaginationParams
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return CrimeTypeService(CrimeTypeRepository(db))


@router.get("/", response_model=PaginatedResponse)
async def list_crime_types(page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    params = PaginationParams(page=page, page_size=page_size)
    return success_response(data=(await svc.get_paginated(params)).model_dump())


@router.get("/{crimetype_id}")
async def get_crime_type(crimetype_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    ct = await svc.get_by_id(crimetype_id)
    if not ct:
        return success_response(message="Crime type not found")
    return success_response(data=CrimeTypeResponse.model_validate(ct).model_dump())


@router.post("/")
async def create_crime_type(data: CrimeTypeCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    ct = await svc.create(data.model_dump())
    return success_response(data=CrimeTypeResponse.model_validate(ct).model_dump(), message="Crime type created")


@router.delete("/{crimetype_id}")
async def delete_crime_type(crimetype_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.delete(crimetype_id)
    return success_response(message="Crime type deleted" if deleted else "Crime type not found")
