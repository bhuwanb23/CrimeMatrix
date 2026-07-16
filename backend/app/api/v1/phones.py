from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.phone_repo import PhoneRepository
from app.services.phone_service import PhoneService
from app.schemas.phone import PhoneCreate, PhoneResponse
from app.schemas.common import PaginatedResponse, PaginationParams
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return PhoneService(PhoneRepository(db))


@router.get("/", )
async def list_phones(page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    params = PaginationParams(page=page, page_size=page_size)
    result = await svc.get_paginated(params); return {"success": True, "data": {"items": [{"id": i.id, "title": getattr(i, "title", getattr(i, "name", "")), "status": getattr(i, "status", "")} for i in result.items], "total": result.total, "page": result.page, "page_size": result.page_size, "total_pages": result.total_pages}, "message": "Success"}


@router.get("/{phone_id}")
async def get_phone(phone_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    phone = await svc.get_by_id(phone_id)
    if not phone:
        return success_response(message="Phone not found")
    return success_response(data=PhoneResponse.model_validate(phone).model_dump())


@router.post("/")
async def create_phone(data: PhoneCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    phone = await svc.create(data.model_dump())
    return success_response(data=PhoneResponse.model_validate(phone).model_dump(), message="Phone created")


@router.delete("/{phone_id}")
async def delete_phone(phone_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.delete(phone_id)
    return success_response(message="Phone deleted" if deleted else "Phone not found")


@router.get("/number/{number}")
async def get_by_number(number: str, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    phone = await svc.get_by_number(number)
    if not phone:
        return success_response(message="Phone not found")
    return success_response(data=PhoneResponse.model_validate(phone).model_dump())

