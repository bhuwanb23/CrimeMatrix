from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.person_repo import PersonRepository
from app.services.person_service import PersonService
from app.schemas.person import PersonCreate, PersonResponse
from app.schemas.common import PaginatedResponse, PaginationParams
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return PersonService(PersonRepository(db))


@router.get("/")
async def list_persons(page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    params = PaginationParams(page=page, page_size=page_size)
    result = await svc.get_paginated(params)
    return {"success": True, "data": {"items": [{"id": p.id, "first_name": p.first_name, "last_name": p.last_name, "district": p.district} for p in result.items], "total": result.total, "page": result.page, "page_size": result.page_size, "total_pages": result.total_pages}, "message": "Success"}


@router.get("/{person_id}")
async def get_person(person_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    person = await svc.get_by_id(person_id)
    if not person:
        return success_response(message="Person not found")
    return success_response(data=PersonResponse.model_validate(person).model_dump())


@router.post("/")
async def create_person(data: PersonCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    person = await svc.create(data.model_dump())
    return success_response(data=PersonResponse.model_validate(person).model_dump(), message="Person created")


@router.put("/{person_id}")
async def update_person(person_id: int, data: PersonCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    person = await svc.update(person_id, data.model_dump(exclude_unset=True))
    if not person:
        return success_response(message="Person not found")
    return success_response(data=PersonResponse.model_validate(person).model_dump(), message="Person updated")


@router.delete("/{person_id}")
async def delete_person(person_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.delete(person_id)
    return success_response(message="Person deleted" if deleted else "Person not found")


@router.get("/search/{query}")
async def search_persons(query: str, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    results = await svc.search_persons(query)
    return success_response(data=[PersonResponse.model_validate(r).model_dump() for r in results])
