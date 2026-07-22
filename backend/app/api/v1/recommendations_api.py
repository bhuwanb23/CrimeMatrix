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


class FeedbackRequest(BaseModel):
    feedback: str


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


@router.get("/all")
async def all_recommendations(
    rec_type: Optional[str] = Query(default=None),
    status: str = Query(default="active"),
    limit: int = Query(default=20),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.get_all_recommendations(rec_type=rec_type, status=status, limit=limit)
    return success_response(data=result)


@router.post("/{recommendation_id}/feedback")
async def submit_feedback(
    recommendation_id: int,
    data: FeedbackRequest,
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.provide_feedback(recommendation_id, data.feedback)
    if "error" in result:
        return success_response(data=result, message=result["error"])
    return success_response(data=result, message="Feedback recorded")


@router.get("/history")
async def recommendation_history(
    recommendation_id: Optional[int] = Query(default=None),
    limit: int = Query(default=50),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.get_recommendation_history(recommendation_id=recommendation_id, limit=limit)
    return success_response(data=result)


@router.post("/generate")
async def generate_recommendations(
    context_type: str = Query(default="dashboard"),
    entity_id: Optional[int] = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.generate_and_persist(context_type=context_type, entity_id=entity_id)
    return success_response(data=result, message="Recommendations generated")
