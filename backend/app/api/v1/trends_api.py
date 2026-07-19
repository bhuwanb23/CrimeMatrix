from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, List
from app.db.session import get_db
from app.services.trend_analysis_service import TrendAnalysisService
from app.core.response import success_response

router = APIRouter()


class SnapshotCreate(BaseModel):
    metric_name: str
    metric_value: float
    comparison_value: Optional[float] = None


def get_service(db: AsyncSession):
    return TrendAnalysisService(db)


@router.get("/summary")
async def trend_summary(
    period: str = Query(default="daily"),
    district_id: int = Query(default=None),
    crime_type_id: int = Query(default=None),
    days: int = Query(default=30),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.get_summary(period, district_id, crime_type_id, days))


@router.get("/daily")
async def daily_trends(
    days: int = Query(default=30),
    district_id: int = Query(default=None),
    crime_type_id: int = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.get_daily_trends(days, district_id, crime_type_id))


@router.get("/weekly")
async def weekly_trends(
    weeks: int = Query(default=12),
    district_id: int = Query(default=None),
    crime_type_id: int = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.get_weekly_trends(weeks, district_id, crime_type_id))


@router.get("/monthly")
async def monthly_trends(
    months: int = Query(default=12),
    district_id: int = Query(default=None),
    crime_type_id: int = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.get_monthly_trends(months, district_id, crime_type_id))


@router.get("/yearly")
async def yearly_trends(
    years: int = Query(default=5),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.get_yearly_trends(years))


@router.get("/district/{district_id}")
async def district_trends(
    district_id: int,
    days: int = Query(default=30),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.get_district_trends(district_id, days))


@router.get("/compare-districts")
async def compare_districts(
    ids: str = Query(..., description="Comma-separated district IDs"),
    days: int = Query(default=30),
    db: AsyncSession = Depends(get_db),
):
    district_ids = [int(x.strip()) for x in ids.split(",") if x.strip().isdigit()]
    svc = get_service(db)
    return success_response(data=await svc.compare_districts(district_ids, days))


@router.get("/seasonal")
async def seasonal_patterns(
    days: int = Query(default=365),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.get_seasonal_patterns(days))


@router.get("/crime-types")
async def crime_type_trends(
    days: int = Query(default=30),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.get_crime_type_trends(days))


@router.get("/snapshots")
async def get_snapshots(
    metric_name: str = Query(default=None),
    limit: int = Query(default=30),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.get_snapshots(metric_name, limit))


@router.post("/snapshots")
async def create_snapshot(data: SnapshotCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.create_snapshot(data.metric_name, data.metric_value, data.comparison_value)
    return success_response(data=result, message="Snapshot created")
