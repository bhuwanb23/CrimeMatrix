from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.session import get_db
from app.services.intelligence_timeline_service import IntelligenceTimelineService
from app.core.response import success_response

router = APIRouter()


def get_service(db: AsyncSession):
    return IntelligenceTimelineService(db)


@router.get("/")
async def unified_timeline(
    source: Optional[str] = Query(default=None, description="Filter by source: event, alert, evidence, recommendation, risk, match"),
    entity_type: Optional[str] = Query(default=None, description="Filter by entity type"),
    limit: int = Query(default=50),
    offset: int = Query(default=0),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.get_unified_timeline(limit=limit, offset=offset, source=source, entity_type=entity_type)
    return success_response(data=result)


@router.get("/events")
async def event_history(limit: int = Query(default=30), db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.get_event_history(limit=limit)
    return success_response(data=result)


@router.get("/alerts")
async def alert_history(limit: int = Query(default=30), db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.get_alert_history(limit=limit)
    return success_response(data=result)


@router.get("/evidence")
async def evidence_history(limit: int = Query(default=30), db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.get_evidence_history(limit=limit)
    return success_response(data=result)


@router.get("/recommendations")
async def recommendation_history(limit: int = Query(default=30), db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.get_recommendation_history(limit=limit)
    return success_response(data=result)


@router.get("/risk")
async def risk_history(limit: int = Query(default=30), db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.get_risk_history(limit=limit)
    return success_response(data=result)


@router.get("/stats")
async def timeline_stats(db: AsyncSession = Depends(get_db)):
    from app.db.phase1_store import using_phase1_store

    if using_phase1_store():
        from app.db.phase1_aggregations import (
            derive_early_alerts,
            derive_timeline_entries,
            fetch_all_safe,
            intelligence_timeline_stats,
            resolve_names,
        )

        crimes = await fetch_all_safe("crimes")
        investigations = await fetch_all_safe("investigations")
        events = await fetch_all_safe("timeline_events")
        alerts = derive_early_alerts(
            crimes, await resolve_names("districts"), await resolve_names("crime_types")
        )
        derived = derive_timeline_entries(crimes, investigations, events, limit=1, offset=0)
        return success_response(data=intelligence_timeline_stats({
            "events": len(events),
            "processed": len(crimes),
            "alerts": len(alerts),
            "early_warnings": sum(1 for a in alerts if a.get("severity") in {"high", "critical"}),
            "evidence_links": len(await fetch_all_safe("evidence")),
            "link_history": 0,
            "match_history": 0,
            "cross_district": 0,
            "recommendation_history": len(investigations),
            "risk_history": len(await fetch_all_safe("suspects")),
            "priority_history": len(investigations),
            "unified_entries": derived["total_count"],
        }))
    svc = get_service(db)
    result = await svc.get_timeline_stats()
    return success_response(data=result)
