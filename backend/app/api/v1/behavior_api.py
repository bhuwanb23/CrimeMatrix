from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.behavior_service import BehaviorService
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return BehaviorService(db)


@router.get("/stats")
async def behavior_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/profiles")
async def list_profiles(
    criminal_id: int = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    profiles = await svc.get_profiles(criminal_id)
    return success_response(data={"items": profiles, "total": len(profiles)})


@router.post("/analyze/{criminal_id}")
async def analyze_criminal(criminal_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.analyze_criminal(criminal_id)
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result, message="Behavioral profile generated")


@router.get("/risk-assessment")
async def risk_assessment(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_risk_assessment())


@router.get("/features/{profile_id}")
async def get_features(profile_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    features = await svc.get_features(profile_id)
    return success_response(data={"items": features, "total": len(features)})
