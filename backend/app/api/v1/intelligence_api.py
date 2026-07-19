from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.intelligence_service import IntelligenceService
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return IntelligenceService(db)


@router.get("/summary")
async def intelligence_summary(
    district: str = Query(default=None),
    time_range: str = Query(default="30d"),
    crime_type: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    data = await svc.get_summary(district=district, time_range=time_range, crime_type=crime_type)
    return success_response(data=data)


@router.get("/trends")
async def intelligence_trends(
    time_range: str = Query(default="30d"),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    data = await svc._get_trends(time_range)
    return success_response(data=data)


@router.get("/hotspots")
async def intelligence_hotspots(
    time_range: str = Query(default="30d"),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    data = await svc._get_hotspots(time_range)
    return success_response(data=data)
