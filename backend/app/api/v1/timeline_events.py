from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.timeline_repo import TimelineRepository
from app.schemas.timeline import TimelineEventCreate, TimelineEventResponse
from app.core.response import success_response

router = APIRouter()


@router.get("/investigation/{investigation_id}")
async def list_events(investigation_id: int, db: AsyncSession = Depends(get_db)):
    repo = TimelineRepository(db)
    events = await repo.get_by_investigation(investigation_id)
    return success_response(data=[TimelineEventResponse.model_validate(e).model_dump() for e in events])


@router.post("/")
async def create_event(data: TimelineEventCreate, db: AsyncSession = Depends(get_db)):
    repo = TimelineRepository(db)
    event = await repo.create(data.model_dump())
    return success_response(data=TimelineEventResponse.model_validate(event).model_dump(), message="Event created")


@router.delete("/{event_id}")
async def delete_event(event_id: int, db: AsyncSession = Depends(get_db)):
    repo = TimelineRepository(db)
    deleted = await repo.delete(event_id)
    return success_response(message="Event deleted" if deleted else "Event not found")
