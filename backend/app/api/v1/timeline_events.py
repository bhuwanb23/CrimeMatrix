from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.timeline_repo import TimelineRepository
from app.schemas.timeline import TimelineEventCreate, TimelineEventResponse
from app.core.response import success_response
from app.db.phase1_store import store_create, store_delete, store_list, using_phase1_store

router = APIRouter()


@router.get("/investigation/{investigation_id}")
async def list_events(investigation_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        data = await store_list(
            "timeline_events",
            page=1,
            page_size=100,
            where={"investigation_id": investigation_id},
        )
        return success_response(data=data["items"])
    repo = TimelineRepository(db)
    events = await repo.get_by_investigation(investigation_id)
    return success_response(data=[TimelineEventResponse.model_validate(e).model_dump() for e in events])


@router.post("/")
async def create_event(data: TimelineEventCreate, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        event = await store_create("timeline_events", data.model_dump())
        return success_response(data=event, message="Event created")
    repo = TimelineRepository(db)
    event = await repo.create(data.model_dump())
    return success_response(data=TimelineEventResponse.model_validate(event).model_dump(), message="Event created")


@router.delete("/{event_id}")
async def delete_event(event_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        deleted = await store_delete("timeline_events", event_id)
        return success_response(message="Event deleted" if deleted else "Event not found")
    repo = TimelineRepository(db)
    deleted = await repo.delete(event_id)
    return success_response(message="Event deleted" if deleted else "Event not found")
