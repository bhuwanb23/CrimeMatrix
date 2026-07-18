from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.crime_repo import CrimeRepository
from app.services.crime_service import CrimeService
from app.schemas.crime import CrimeCreate, CrimeResponse
from app.schemas.common import PaginatedResponse, PaginationParams
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return CrimeService(CrimeRepository(db))


@router.get("/")
async def list_crimes(page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    params = PaginationParams(page=page, page_size=page_size)
    result = await svc.get_paginated(params)
    return {
        "success": True,
        "data": {
            "items": [{"id": c.id, "title": c.title, "crime_type_id": c.crime_type_id, "district_id": c.district_id, "status": c.status, "priority": c.priority} for c in result.items],
            "total": result.total,
            "page": result.page,
            "page_size": result.page_size,
            "total_pages": result.total_pages,
        },
        "message": "Success",
    }


@router.get("/{crime_id}")
async def get_crime(crime_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    crime = await svc.get_by_id(crime_id)
    if not crime:
        return success_response(message="Crime not found")
    return success_response(data=CrimeResponse.model_validate(crime).model_dump())


@router.post("/")
async def create_crime(data: CrimeCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    crime = await svc.create(data.model_dump())
    return success_response(data=CrimeResponse.model_validate(crime).model_dump(), message="Crime created")


@router.put("/{crime_id}")
async def update_crime(crime_id: int, data: CrimeCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    crime = await svc.update(crime_id, data.model_dump(exclude_unset=True))
    if not crime:
        return success_response(message="Crime not found")
    return success_response(data=CrimeResponse.model_validate(crime).model_dump(), message="Crime updated")


@router.delete("/{crime_id}")
async def delete_crime(crime_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.delete(crime_id)
    return success_response(message="Crime deleted" if deleted else "Crime not found")


@router.get("/search/{query}")
async def search_crimes(query: str, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    results = await svc.search_crimes(query)
    return success_response(data=[CrimeResponse.model_validate(r).model_dump() for r in results])
