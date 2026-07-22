from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.db.session import get_db
from app.services.event_processing_service import EventProcessingService
from app.core.response import success_response

router = APIRouter()


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
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/events")
async def list_events(
    status: str = Query(default=None),
    event_type: str = Query(default=None),
    limit: int = Query(default=50),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    events = await svc.get_events(status, event_type, limit)
    return success_response(data={"items": events, "total": len(events)})


@router.get("/events/{event_id}")
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    event = await svc.get_event(event_id)
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
    svc = get_service(db)
    queue = await svc.get_queue()
    return success_response(data={"items": queue, "total": len(queue)})


@router.get("/processed")
async def processed_events(
    limit: int = Query(default=20),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    processed = await svc.get_processed(limit)
    return success_response(data={"items": processed, "total": len(processed)})


@router.post("/scan")
async def scan_data(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.scan_for_new_data()
    return success_response(data=result, message="Scan complete")


@router.get("/activity")
async def activity_feed(
    limit: int = Query(default=20),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    activity = await svc.get_activity(limit)
    return success_response(data={"items": activity, "total": len(activity)})


@router.post("/batch-process")
async def batch_process(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.batch_process()
    return success_response(data=result, message="Batch processing complete")
