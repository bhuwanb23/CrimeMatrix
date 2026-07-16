from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.crime import Crime
import structlog

logger = structlog.get_logger()


class EvidenceExporter:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def export_json(self, crime_id: int) -> Dict[str, Any]:
        crime = (await self.db.execute(
            select(Crime).where(Crime.id == crime_id)
        )).scalar_one_or_none()

        if not crime:
            return {"error": "Crime not found"}

        evidence = []
        if crime.description:
            evidence.append({
                "title": crime.title,
                "type": "case_description",
                "description": crime.description,
                "collected_at": str(crime.created_at)[:19] if crime.created_at else "N/A",
                "officer": "System",
            })

        return {
            "crime_id": crime.id,
            "title": crime.title,
            "status": crime.status,
            "evidence": evidence,
            "total_evidence": len(evidence),
        }
