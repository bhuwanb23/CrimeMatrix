import json
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.intelligence_event import IntelligenceEvent
from app.models.event_queue_record import EventQueueRecord
from app.models.processed_event import ProcessedEvent
from app.models.crime import Crime
from app.models.evidence import Evidence
from app.models.investigation import Investigation
import structlog
from datetime import datetime, timedelta

logger = structlog.get_logger()


class EventProcessingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_event(self, event_type: str, entity_id: int = None,
                           entity_type: str = None, event_data: str = None,
                           created_by: str = "system") -> dict:
        event = IntelligenceEvent(
            event_type=event_type,
            entity_id=entity_id,
            entity_type=entity_type,
            event_data=event_data,
            status="pending",
            created_by=created_by,
        )
        self.db.add(event)
        await self.db.flush()

        # Add to queue
        queue = EventQueueRecord(
            event_id=event.id,
            priority="medium",
            status="queued",
        )
        self.db.add(queue)
        await self.db.commit()

        return {"id": event.id, "event_type": event_type, "status": "queued"}

    async def get_events(self, status: str = None, event_type: str = None,
                         limit: int = 50) -> List[dict]:
        stmt = select(IntelligenceEvent)
        if status:
            stmt = stmt.where(IntelligenceEvent.status == status)
        if event_type:
            stmt = stmt.where(IntelligenceEvent.event_type == event_type)
        stmt = stmt.order_by(IntelligenceEvent.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return [
            {"id": e.id, "event_type": e.event_type, "entity_id": e.entity_id,
             "entity_type": e.entity_type, "status": e.status, "created_by": e.created_by,
             "created_at": str(e.created_at) if e.created_at else None,
             "processed_at": str(e.processed_at) if e.processed_at else None}
            for e in result.scalars().all()
        ]

    async def get_event(self, event_id: int) -> Optional[dict]:
        stmt = select(IntelligenceEvent).where(IntelligenceEvent.id == event_id)
        result = await self.db.execute(stmt)
        e = result.scalar()
        if not e:
            return None
        return {
            "id": e.id, "event_type": e.event_type, "entity_id": e.entity_id,
            "entity_type": e.entity_type, "event_data": e.event_data,
            "status": e.status, "created_by": e.created_by,
            "created_at": str(e.created_at) if e.created_at else None,
            "processed_at": str(e.processed_at) if e.processed_at else None,
        }

    async def process_pending(self) -> dict:
        stmt = select(IntelligenceEvent).where(IntelligenceEvent.status == "pending").limit(10)
        result = await self.db.execute(stmt)
        events = result.scalars().all()
        processed = 0
        for event in events:
            event.status = "processed"
            event.processed_at = datetime.utcnow()
            pe = ProcessedEvent(
                event_id=event.id,
                processor_name="auto_processor",
                result=json.dumps({"status": "processed"}),
                duration_ms=0,
            )
            self.db.add(pe)
            processed += 1
        await self.db.commit()
        return {"processed": processed}

    async def get_queue(self) -> List[dict]:
        stmt = select(EventQueueRecord).where(EventQueueRecord.status == "queued").order_by(EventQueueRecord.created_at.desc())
        result = await self.db.execute(stmt)
        return [
            {"id": q.id, "event_id": q.event_id, "priority": q.priority,
             "status": q.status, "retry_count": q.retry_count,
             "created_at": str(q.created_at) if q.created_at else None}
            for q in result.scalars().all()
        ]

    async def get_processed(self, limit: int = 20) -> List[dict]:
        stmt = select(ProcessedEvent).order_by(ProcessedEvent.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return [
            {"id": p.id, "event_id": p.event_id, "processor_name": p.processor_name,
             "duration_ms": p.duration_ms,
             "created_at": str(p.created_at) if p.created_at else None}
            for p in result.scalars().all()
        ]

    async def scan_for_new_data(self) -> dict:
        # Check for new crimes
        date_from = datetime.utcnow() - timedelta(hours=1)
        new_crimes = (await self.db.execute(
            select(sql_func.count(Crime.id)).where(Crime.created_at >= date_from)
        )).scalar() or 0

        # Check for new evidence
        new_evidence = (await self.db.execute(
            select(sql_func.count(Evidence.id)).where(Evidence.created_at >= date_from)
        )).scalar() or 0

        # Create events for new data
        events_created = 0
        if new_crimes > 0:
            await self.create_event("crime_update", event_data=json.dumps({"count": new_crimes}))
            events_created += 1
        if new_evidence > 0:
            await self.create_event("evidence_update", event_data=json.dumps({"count": new_evidence}))
            events_created += 1

        return {
            "new_crimes": new_crimes,
            "new_evidence": new_evidence,
            "events_created": events_created,
            "scan_time": datetime.utcnow().isoformat(),
        }

    async def get_activity(self, limit: int = 20) -> List[dict]:
        stmt = select(IntelligenceEvent).order_by(IntelligenceEvent.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return [
            {"id": e.id, "event_type": e.event_type, "entity_id": e.entity_id,
             "status": e.status, "created_by": e.created_by,
             "created_at": str(e.created_at) if e.created_at else None}
            for e in result.scalars().all()
        ]

    async def get_stats(self) -> dict:
        total = (await self.db.execute(select(sql_func.count(IntelligenceEvent.id)))).scalar() or 0
        pending = (await self.db.execute(
            select(sql_func.count(IntelligenceEvent.id)).where(IntelligenceEvent.status == "pending")
        )).scalar() or 0
        processed = (await self.db.execute(
            select(sql_func.count(ProcessedEvent.id))
        )).scalar() or 0
        queued = (await self.db.execute(
            select(sql_func.count(EventQueueRecord.id)).where(EventQueueRecord.status == "queued")
        )).scalar() or 0
        return {"total_events": total, "pending": pending, "processed": processed, "queued": queued}
