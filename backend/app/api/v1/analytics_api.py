from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.analytics.statistics import StatisticsEngine
from app.analytics.aggregations import AggregationEngine
from app.analytics.heatmaps import HeatmapEngine
from app.analytics.trends import TrendEngine
from app.analytics.districts import DistrictAnalytics
from app.analytics.crime_counts import CrimeCountEngine
from app.analytics.time_series import TimeSeriesEngine
from app.core.response import success_response
from pydantic import BaseModel
from typing import Optional, Dict, Any

router = APIRouter()


class AggregateRequest(BaseModel):
    entity: str
    group_by: str
    metric: str = "count"


# Statistics
@router.get("/stats/overview")
async def stats_overview(db: AsyncSession = Depends(get_db)):
    engine = StatisticsEngine(db)
    data = await engine.get_overview()
    return success_response(data=data)


@router.get("/stats/summary")
async def stats_summary(db: AsyncSession = Depends(get_db)):
    engine = StatisticsEngine(db)
    data = await engine.get_summary()
    return success_response(data=data)


# Aggregations
@router.post("/aggregate")
async def aggregate(data: AggregateRequest, db: AsyncSession = Depends(get_db)):
    engine = AggregationEngine(db)
    result = await engine.aggregate(data.entity, data.group_by, data.metric)
    return success_response(data=result)


# Heatmaps
@router.get("/heatmap/district")
async def district_heatmap(db: AsyncSession = Depends(get_db)):
    engine = HeatmapEngine(db)
    data = await engine.district_heatmap()
    return success_response(data=data)


@router.get("/heatmap/timeline")
async def timeline_heatmap(db: AsyncSession = Depends(get_db)):
    engine = HeatmapEngine(db)
    data = await engine.timeline_heatmap()
    return success_response(data=data)


# Trends
@router.get("/trends/crimes")
async def crime_trends(
    period: str = "daily",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    engine = TrendEngine(db)
    data = await engine.crime_trends(period, start_date, end_date)
    return success_response(data=data)


@router.get("/trends/cases")
async def case_trends(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    engine = TrendEngine(db)
    data = await engine.case_trends(start_date, end_date)
    return success_response(data=data)


@router.get("/trends/resolution")
async def resolution_trend(db: AsyncSession = Depends(get_db)):
    engine = TrendEngine(db)
    data = await engine.resolution_trend()
    return success_response(data=data)


# District Analytics
@router.get("/districts")
async def all_districts(db: AsyncSession = Depends(get_db)):
    engine = DistrictAnalytics(db)
    data = await engine.get_all_districts()
    return success_response(data=data)


@router.get("/districts/{district_id}")
async def district_detail(district_id: int, db: AsyncSession = Depends(get_db)):
    engine = DistrictAnalytics(db)
    data = await engine.get_district_detail(district_id)
    return success_response(data=data)


# Crime Counts
@router.get("/counts/by-type")
async def count_by_type(db: AsyncSession = Depends(get_db)):
    engine = CrimeCountEngine(db)
    data = await engine.count_by_type()
    return success_response(data=data)


@router.get("/counts/by-status")
async def count_by_status(db: AsyncSession = Depends(get_db)):
    engine = CrimeCountEngine(db)
    data = await engine.count_by_status()
    return success_response(data=data)


@router.get("/counts/by-district")
async def count_by_district(db: AsyncSession = Depends(get_db)):
    engine = CrimeCountEngine(db)
    data = await engine.count_by_district()
    return success_response(data=data)


@router.get("/counts/by-priority")
async def count_by_priority(db: AsyncSession = Depends(get_db)):
    engine = CrimeCountEngine(db)
    data = await engine.count_by_priority()
    return success_response(data=data)


# Time Series
@router.get("/timeseries/crimes")
async def crime_time_series(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    engine = TimeSeriesEngine(db)
    data = await engine.crime_series(start_date, end_date)
    return success_response(data=data)


@router.get("/timeseries/cases")
async def case_time_series(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    engine = TimeSeriesEngine(db)
    data = await engine.case_series(start_date, end_date)
    return success_response(data=data)


@router.get("/timeseries/activity")
async def activity_time_series(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    engine = TimeSeriesEngine(db)
    data = await engine.activity_series(start_date, end_date)
    return success_response(data=data)
