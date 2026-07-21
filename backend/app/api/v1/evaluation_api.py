from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.db.session import get_db
from app.services.evaluation_service import EvaluationService
from app.core.response import success_response

router = APIRouter()


class MetricRecordRequest(BaseModel):
    model_name: str
    metric_name: str
    metric_value: float
    period_type: str = "daily"
    metadata_json: Optional[str] = None


class FeedbackRequest(BaseModel):
    prediction_id: int
    user_id: int = 1
    feedback_type: str = "correct"
    rating: int = 5
    comment: Optional[str] = None


def get_service(db: AsyncSession):
    return EvaluationService(db)


@router.get("/stats")
async def evaluation_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/metrics")
async def list_metrics(
    model_name: str = Query(default=None),
    metric_name: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    metrics = await svc.get_metrics(model_name, metric_name)
    return success_response(data={"items": metrics, "total": len(metrics)})


@router.post("/metrics")
async def record_metric(data: MetricRecordRequest, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.record_metric(data.model_name, data.metric_name, data.metric_value, data.period_type, data.metadata_json)
    return success_response(data=result, message="Metric recorded")


@router.get("/feedback")
async def list_feedback(
    prediction_id: int = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    feedback = await svc.get_feedback(prediction_id)
    return success_response(data={"items": feedback, "total": len(feedback)})


@router.post("/feedback")
async def submit_feedback(data: FeedbackRequest, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.submit_feedback(data.prediction_id, data.user_id, data.feedback_type, data.rating, data.comment)
    return success_response(data=result, message="Feedback submitted")


@router.get("/results")
async def list_results(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    results = await svc.get_results()
    return success_response(data={"items": results, "total": len(results)})


@router.post("/run")
async def run_evaluation(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.run_evaluation()
    return success_response(data=result, message="Evaluation complete")


@router.get("/accuracy-trend")
async def accuracy_trend(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    trend = await svc.get_accuracy_trend()
    return success_response(data=trend)


@router.get("/drift")
async def drift(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_drift())
