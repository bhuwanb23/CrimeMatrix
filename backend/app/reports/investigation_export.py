from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.crime import Crime
from app.reports.timeline_export import TimelineExporter
from app.reports.evidence_export import EvidenceExporter
import structlog

logger = structlog.get_logger()


class InvestigationExporter:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.timeline = TimelineExporter(db)
        self.evidence = EvidenceExporter(db)

    async def export_json(self, crime_id: int) -> Dict[str, Any]:
        crime = (await self.db.execute(
            select(Crime).where(Crime.id == crime_id)
        )).scalar_one_or_none()

        if not crime:
            return {"error": "Crime not found"}

        timeline_data = await self.timeline.export_json(crime_id)
        evidence_data = await self.evidence.export_json(crime_id)

        return {
            "crime_id": crime.id,
            "title": crime.title,
            "description": crime.description,
            "status": crime.status,
            "priority": crime.priority,
            "crime_type_id": crime.crime_type_id,
            "district_id": crime.district_id,
            "location_id": crime.location_id,
            "created_at": str(crime.created_at)[:19] if crime.created_at else None,
            "occurred_at": str(crime.occurred_at)[:19] if crime.occurred_at else None,
            "timeline": timeline_data.get("events", []),
            "evidence": evidence_data.get("evidence", []),
            "notes": [],
        }
