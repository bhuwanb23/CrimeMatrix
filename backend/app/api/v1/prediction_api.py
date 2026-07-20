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


# Forecast-specific endpoints
from app.services.forecast_service import ForecastService


@router.post("/forecast/district")
async def forecast_district(data: ForecastRequest, db: AsyncSession = Depends(get_db)):
    svc = ForecastService(db)
    if not data.district_id:
        return success_response(message="district_id required")
    result = await svc.forecast_district(data.district_id, data.periods)
    return success_response(data=result, message="District forecast generated")


@router.post("/forecast/category")
async def forecast_category(data: ForecastRequest, db: AsyncSession = Depends(get_db)):
    svc = ForecastService(db)
    if not data.crime_type_id:
        return success_response(message="crime_type_id required")
    result = await svc.forecast_category(data.crime_type_id, data.periods)
    return success_response(data=result, message="Category forecast generated")


@router.get("/forecast/seasonal")
async def forecast_seasonal(
    days: int = Query(default=365),
    db: AsyncSession = Depends(get_db),
):
    svc = ForecastService(db)
    result = await svc.get_seasonal_patterns(days)
    return success_response(data=result)


@router.get("/forecast/history")
async def forecast_history(
    limit: int = Query(default=30),
    db: AsyncSession = Depends(get_db),
):
    svc = ForecastService(db)
    result = await svc.get_forecast_history(limit)
    return success_response(data={"items": result, "total": len(result)})


@router.get("/forecast/stats")
async def forecast_stats(db: AsyncSession = Depends(get_db)):
    svc = ForecastService(db)
    return success_response(data=await svc.get_forecast_stats())


# Explanation endpoints
from app.services.explanation_service import ExplanationService


@router.post("/explain/{prediction_id}")
async def explain_prediction(prediction_id: int, db: AsyncSession = Depends(get_db)):
    svc = ExplanationService(db)
    result = await svc.explain_prediction(prediction_id)
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result, message="Explanation generated")


@router.get("/explain/{prediction_id}")
async def get_explanation(prediction_id: int, db: AsyncSession = Depends(get_db)):
    svc = ExplanationService(db)
    result = await svc.get_explanation(prediction_id)
    if not result:
        return success_response(message="No explanation found")
    return success_response(data=result)


@router.get("/sources/{prediction_id}")
async def get_sources(prediction_id: int, db: AsyncSession = Depends(get_db)):
    svc = ExplanationService(db)
    sources = await svc.get_sources(prediction_id)
    return success_response(data={"items": sources, "total": len(sources)})


@router.get("/confidence/{prediction_id}")
async def get_confidence(prediction_id: int, db: AsyncSession = Depends(get_db)):
    svc = ExplanationService(db)
    result = await svc.get_confidence_breakdown(prediction_id)
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result)
