from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.intelligence_service import IntelligenceService
from app.core.response import success_response
from app.db.phase1_store import using_phase1_store

router = APIRouter()


def get_service(db: AsyncSession):
    return IntelligenceService(db)


async def _phase1_summary(district: str = None, time_range: str = "30d", crime_type: str = None):
    from app.db.phase1_aggregations import fetch_all_safe, geo_context
    from app.db.phase1_aggregations import intelligence_summary as build_summary

    ctx = await geo_context()
    return build_summary(
        ctx,
        criminals=await fetch_all_safe("criminals"),
        investigations=await fetch_all_safe("investigations"),
        victims=await fetch_all_safe("victims"),
        witnesses=await fetch_all_safe("witnesses"),
        district=district,
        time_range=time_range,
        crime_type=crime_type,
    )


@router.get("/summary")
async def intelligence_summary(
    district: str = Query(default=None),
    time_range: str = Query(default="30d"),
    crime_type: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        return success_response(data=await _phase1_summary(district, time_range, crime_type))
    svc = get_service(db)
    data = await svc.get_summary(district=district, time_range=time_range, crime_type=crime_type)
    return success_response(data=data)


@router.get("/trends")
async def intelligence_trends(
    time_range: str = Query(default="30d"),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        summary = await _phase1_summary(time_range=time_range)
        return success_response(data=summary["trends"])
    svc = get_service(db)
    data = await svc._get_trends(time_range)
    return success_response(data=data)


@router.get("/hotspots")
async def intelligence_hotspots(
    time_range: str = Query(default="30d"),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        summary = await _phase1_summary(time_range=time_range)
        return success_response(data=summary["hotspots"])
    svc = get_service(db)
    data = await svc._get_hotspots(time_range)
    return success_response(data=data)
