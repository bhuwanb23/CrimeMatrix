from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.analytics_dashboard_service import AnalyticsDashboardService
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return AnalyticsDashboardService(db)


@router.get("/summary")
async def dashboard_summary(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_summary())


@router.get("/alerts")
async def dashboard_alerts(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_alerts())


@router.get("/forecasts")
async def dashboard_forecasts(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_forecasts())


@router.get("/high-risk")
async def dashboard_high_risk(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_high_risk())


@router.get("/priority")
async def dashboard_priority(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_priority_cases())


@router.get("/stats")
async def dashboard_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_stats())
