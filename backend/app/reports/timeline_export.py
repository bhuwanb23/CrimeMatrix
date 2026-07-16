from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.crime import Crime
import structlog

logger = structlog.get_logger()


class TimelineExporter:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def export_json(self, crime_id: int) -> Dict[str, Any]:
        crime = (await self.db.execute(
            select(Crime).where(Crime.id == crime_id)
        )).scalar_one_or_none()

        if not crime:
            return {"error": "Crime not found"}

        events = []
        if crime.created_at:
            events.append({
                "date": str(crime.created_at)[:19],
                "title": "Crime reported",
                "description": f"{crime.title} reported to police",
            })
        if crime.occurred_at:
            events.append({
                "date": str(crime.occurred_at)[:19],
                "title": "Crime occurred",
                "description": crime.description or crime.title,
            })
        if crime.updated_at and crime.updated_at != crime.created_at:
            events.append({
                "date": str(crime.updated_at)[:19],
                "title": "Record updated",
                "description": f"Crime record was updated",
            })

        events.sort(key=lambda x: x.get("date", ""))

        return {
            "crime_id": crime.id,
            "title": crime.title,
            "status": crime.status,
            "events": events,
            "total_events": len(events),
        }
