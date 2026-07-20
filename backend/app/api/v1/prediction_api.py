from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.db.session import get_db
from app.services.prediction_service import PredictionService
from app.core.response import success_response

router = APIRouter()


class ForecastRequest(BaseModel):
    district_id: Optional[int] = None
    crime_type_id: Optional[int] = None
    periods: int = 30


def get_service(db: AsyncSession):
    return PredictionService(db)


@router.get("/stats")
async def prediction_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/")
async def list_predictions(
    prediction_type: str = Query(default=None),
    district_id: int = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    predictions = await svc.get_predictions(prediction_type, district_id)
    return success_response(data={"items": predictions, "total": len(predictions)})


@router.get("/models")
async def list_models(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    models = await svc.get_models()
    return success_response(data=models)


@router.get("/district/{district_id}")
async def district_predictions(district_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_district_predictions(district_id))


@router.post("/forecast")
async def generate_forecast(data: ForecastRequest, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.forecast(data.district_id, data.crime_type_id, data.periods)
    return success_response(data=result, message="Forecast generated")


@router.get("/{prediction_id}")
async def get_prediction(prediction_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    prediction = await svc.get_prediction(prediction_id)
    if not prediction:
        return success_response(message="Prediction not found")
    return success_response(data=prediction)
