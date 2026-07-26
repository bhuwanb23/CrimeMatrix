from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.db.session import get_db
from app.services.event_processing_service import EventProcessingService
from app.services.intelligence_explanation_service import IntelligenceExplanationService
from app.core.response import success_response
from app.db.phase1_store import using_phase1_store

router = APIRouter()


async def _phase1_events(limit: int = 50):
    from app.db.phase1_aggregations import derive_proactive_events, fetch_all_safe

    return derive_proactive_events(
        await fetch_all_safe("crimes"),
        await fetch_all_safe("investigations"),
        await fetch_all_safe("evidence"),
        limit=limit,
    )


class EventCreateRequest(BaseModel):
    event_type: str
    entity_id: Optional[int] = None
    entity_type: Optional[str] = None
    event_data: Optional[str] = None
    created_by: str = "system"


class ScanRequest(BaseModel):
    pass


def get_service(db: AsyncSession):
    return EventProcessingService(db)


@router.get("/stats")
async def proactive_stats(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import proactive_stats as build_stats

        return success_response(data=build_stats(await _phase1_events(limit=500)))
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/events")
async def list_events(
    status: str = Query(default=None),
    event_type: str = Query(default=None),
    limit: int = Query(default=50),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        events = await _phase1_events(limit=max(limit, 500))
        if status:
            events = [e for e in events if e["status"] == status]
        if event_type:
            events = [e for e in events if e["event_type"] == event_type]
        events = events[:limit]
        return success_response(data={"items": events, "total": len(events)})
    svc = get_service(db)
    events = await svc.get_events(status, event_type, limit)
    return success_response(data={"items": events, "total": len(events)})


@router.get("/events/{event_id}")
async def get_event(event_id: str, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        match = next(
            (e for e in await _phase1_events(limit=500) if str(e["id"]) == str(event_id)), None
        )
        if not match:
            return success_response(message="Event not found")
        return success_response(data=match)
    if not event_id.isdigit():
        return success_response(message="Event not found")
    svc = get_service(db)
    event = await svc.get_event(int(event_id))
    if not event:
        return success_response(message="Event not found")
    return success_response(data=event)


@router.post("/events")
async def create_event(data: EventCreateRequest, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.create_event(data.event_type, data.entity_id, data.entity_type, data.event_data, data.created_by)
    return success_response(data=result, message="Event created")


@router.post("/events/process")
async def process_events(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.process_pending()
    return success_response(data=result, message="Events processed")


@router.get("/queue")
async def event_queue(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        queue = [e for e in await _phase1_events(limit=500) if e["status"] == "pending"]
        return success_response(data={"items": queue, "total": len(queue)})
    svc = get_service(db)
    queue = await svc.get_queue()
    return success_response(data={"items": queue, "total": len(queue)})


@router.get("/processed")
async def processed_events(
    limit: int = Query(default=20),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        processed = [e for e in await _phase1_events(limit=500) if e["status"] == "processed"]
        processed = processed[:limit]
        return success_response(data={"items": processed, "total": len(processed)})
    svc = get_service(db)
    processed = await svc.get_processed(limit)
    return success_response(data={"items": processed, "total": len(processed)})


@router.post("/scan")
async def scan_data(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import fetch_all_safe, proactive_scan

        result = proactive_scan(
            await fetch_all_safe("crimes"), await fetch_all_safe("evidence")
        )
        return success_response(data=result, message="Scan complete")
    svc = get_service(db)
    result = await svc.scan_for_new_data()
    return success_response(data=result, message="Scan complete")


@router.get("/activity")
async def activity_feed(
    limit: int = Query(default=20),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        activity = await _phase1_events(limit=limit)
        return success_response(data={"items": activity, "total": len(activity)})
    svc = get_service(db)
    activity = await svc.get_activity(limit)
    return success_response(data={"items": activity, "total": len(activity)})


@router.post("/batch-process")
async def batch_process(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import proactive_stats as build_stats

        stats = build_stats(await _phase1_events(limit=500))
        return success_response(
            data={"processed": stats["processed"], "scanned": stats["total_events"]},
            message="Batch processing complete",
        )
    svc = get_service(db)
    result = await svc.batch_process()
    return success_response(data=result, message="Batch processing complete")


def get_explanation_service(db: AsyncSession):
    return IntelligenceExplanationService(db)


@router.post("/explain/event/{event_id}")
async def explain_event(event_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_explanation_service(db)
    result = await svc.explain_event(event_id)
    if "error" in result:
        return success_response(data=result, message=result["error"])
    return success_response(data=result, message="Explanation generated")


@router.post("/explain/recommendation/{rec_id}")
async def explain_recommendation(rec_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_explanation_service(db)
    result = await svc.explain_recommendation(rec_id)
    if "error" in result:
        return success_response(data=result, message=result["error"])
    return success_response(data=result, message="Explanation generated")


@router.post("/explain/evidence-link/{link_id}")
async def explain_evidence_link(link_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_explanation_service(db)
    result = await svc.explain_evidence_link(link_id)
    if "error" in result:
        return success_response(data=result, message=result["error"])
    return success_response(data=result, message="Explanation generated")


@router.post("/explain/alert/{alert_id}")
async def explain_alert(alert_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_explanation_service(db)
    result = await svc.explain_alert(alert_id)
    if "error" in result:
        return success_response(data=result, message=result["error"])
    return success_response(data=result, message="Explanation generated")
