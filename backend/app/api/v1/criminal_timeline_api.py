from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.timeline_service import TimelineService
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return TimelineService(db)


@router.get("/stats")
async def timeline_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_event_stats())


@router.get("/")
async def full_timeline(
    days: int = Query(default=90),
    event_type: str = Query(default=None),
    investigation_id: int = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.get_full_timeline(days, event_type, investigation_id))


@router.get("/suspect/{suspect_name}")
async def suspect_timeline(
    suspect_name: str,
    days: int = Query(default=90),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.get_suspect_timeline(suspect_name, days))


@router.get("/investigation/{investigation_id}")
async def investigation_timeline(
    investigation_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return success_response(data=await svc.get_investigation_timeline(investigation_id))
