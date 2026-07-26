from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.timeline_service import TimelineService
from app.core.response import success_response
from app.db.phase1_store import using_phase1_store

router = APIRouter()


def get_service(db: AsyncSession):
    return TimelineService(db)


async def _phase1_timeline(event_type: str = None, investigation_id: int = None):
    from app.db.phase1_aggregations import build_criminal_timeline, fetch_all_safe

    return build_criminal_timeline(
        await fetch_all_safe("crimes"),
        await fetch_all_safe("investigations"),
        await fetch_all_safe("timeline_events"),
        event_type=event_type,
        investigation_id=investigation_id,
    )


@router.get("/stats")
async def timeline_stats(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import criminal_timeline_stats

        return success_response(data=criminal_timeline_stats(await _phase1_timeline()))
    svc = get_service(db)
    return success_response(data=await svc.get_event_stats())


@router.get("/")
async def full_timeline(
    days: int = Query(default=90),
    event_type: str = Query(default=None),
    investigation_id: int = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        timeline = await _phase1_timeline(event_type, investigation_id)
        return success_response(data={**timeline, "days": days})
    svc = get_service(db)
    return success_response(data=await svc.get_full_timeline(days, event_type, investigation_id))


@router.get("/suspect/{suspect_name}")
async def suspect_timeline(
    suspect_name: str,
    days: int = Query(default=90),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        from app.db.phase1_aggregations import suspect_timeline as build_suspect_timeline

        return success_response(
            data=build_suspect_timeline(await _phase1_timeline(), suspect_name)
        )
    svc = get_service(db)
    return success_response(data=await svc.get_suspect_timeline(suspect_name, days))


@router.get("/investigation/{investigation_id}")
async def investigation_timeline(
    investigation_id: int,
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        timeline = await _phase1_timeline(investigation_id=investigation_id)
        return success_response(data={
            "investigation_id": investigation_id,
            "events": timeline["events"],
            "total": timeline["total"],
        })
    svc = get_service(db)
    return success_response(data=await svc.get_investigation_timeline(investigation_id))
