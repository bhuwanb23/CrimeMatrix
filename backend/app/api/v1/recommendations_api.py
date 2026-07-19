from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.db.session import get_db
from app.services.recommendation_service import RecommendationService
from app.core.response import success_response

router = APIRouter()


class NaturalLanguageSearchRequest(BaseModel):
    query: str


def get_service(db: AsyncSession):
    return RecommendationService(db)


@router.get("/dashboard")
async def dashboard_recommendations(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.get_dashboard_recommendations()
    return success_response(data=result)


@router.get("/case/{case_id}")
async def case_recommendations(case_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.get_case_recommendations(case_id)
    return success_response(data=result)


@router.get("/investigation/{investigation_id}")
async def investigation_recommendations(investigation_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.get_investigation_recommendations(investigation_id)
    return success_response(data=result)


@router.post("/search/natural-language")
async def natural_language_search(data: NaturalLanguageSearchRequest, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.natural_language_search(data.query)
    return success_response(data=result)
