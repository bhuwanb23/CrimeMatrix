from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.session import get_db
from app.repositories.case_repo import CaseRepository
from app.services.case_service import CaseService
from app.schemas.case import CaseCreate, CaseUpdate, CaseResponse
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return CaseService(CaseRepository(db))


@router.get("/")
async def list_cases(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    district: Optional[str] = None,
    status: Optional[str] = None,
    crime_type: Optional[str] = None,
    case_category_id: Optional[int] = None,
    police_station_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    if district:
        cases = await svc.get_by_district(district)
    elif status:
        cases = await svc.get_by_status(status)
    elif case_category_id:
        cases = await svc.repo.get_by_category(case_category_id)
    elif police_station_id:
        cases = await svc.repo.get_by_station(police_station_id)
    else:
        from app.schemas.common import PaginationParams
        params = PaginationParams(page=page, page_size=page_size)
        result = await svc.get_paginated(params)
        return success_response(data={
            "items": [CaseResponse.model_validate(c).model_dump() for c in result.items],
            "total": result.total,
            "page": result.page,
            "page_size": result.page_size,
            "total_pages": result.total_pages,
        })

    start = (page - 1) * page_size
    paginated = cases[start:start + page_size]
    return success_response(data={
        "items": [CaseResponse.model_validate(c).model_dump() for c in paginated],
        "total": len(cases),
        "page": page,
        "page_size": page_size,
        "total_pages": (len(cases) + page_size - 1) // page_size,
    })


@router.get("/{case_id}")
async def get_case(case_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    case = await svc.get_by_id(case_id)
    if not case:
        return success_response(message="Case not found")
    return success_response(data=CaseResponse.model_validate(case).model_dump())


@router.get("/by-number/{case_number}")
async def get_case_by_number(case_number: str, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    case = await svc.get_by_number(case_number)
    if not case:
        return success_response(message="Case not found")
    return success_response(data=CaseResponse.model_validate(case).model_dump())


@router.get("/by-crime-no/{crime_no}")
async def get_case_by_crime_no(crime_no: str, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    case = await svc.repo.get_by_crime_no(crime_no)
    if not case:
        return success_response(message="Case not found")
    return success_response(data=CaseResponse.model_validate(case).model_dump())


@router.post("/")
async def create_case(data: CaseCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    case = await svc.create(data.model_dump(exclude_unset=True))
    return success_response(data=CaseResponse.model_validate(case).model_dump(), message="Case created")


@router.put("/{case_id}")
async def update_case(case_id: int, data: CaseUpdate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    case = await svc.update(case_id, data.model_dump(exclude_unset=True))
    if not case:
        return success_response(message="Case not found")
    return success_response(data=CaseResponse.model_validate(case).model_dump(), message="Case updated")


@router.delete("/{case_id}")
async def delete_case(case_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.delete(case_id)
    return success_response(message="Case deleted" if deleted else "Case not found")


@router.get("/search/{query}")
async def search_cases(query: str, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    results = await svc.search_cases(query)
    return success_response(data=[CaseResponse.model_validate(r).model_dump() for r in results])
