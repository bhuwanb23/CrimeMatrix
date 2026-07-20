from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func, or_
from app.models.timeline_event import TimelineEvent
from app.models.investigation import Investigation
from app.models.case_status_log import CaseStatusLog
from app.models.crime import Crime
import structlog
from datetime import datetime, timedelta
from collections import defaultdict

logger = structlog.get_logger()


class TimelineService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_full_timeline(self, days: int = 90, event_type: str = None,
                                 investigation_id: int = None) -> dict:
        date_from = datetime.utcnow() - timedelta(days=days)

        # Timeline events
        stmt = select(TimelineEvent).where(TimelineEvent.created_at >= date_from)
        if event_type:
            stmt = stmt.where(TimelineEvent.event_type == event_type)
        if investigation_id:
            stmt = stmt.where(TimelineEvent.investigation_id == investigation_id)
        stmt = stmt.order_by(TimelineEvent.event_date.desc().nullslast(), TimelineEvent.created_at.desc())
        result = await self.db.execute(stmt)
        events = result.scalars().all()

        # Case status logs
        stmt2 = select(CaseStatusLog).where(CaseStatusLog.changed_at >= date_from)
        stmt2 = stmt2.order_by(CaseStatusLog.changed_at.desc())
        result2 = await self.db.execute(stmt2)
        status_logs = result2.scalars().all()

        # Combine into unified timeline
        timeline = []
        for e in events:
            timeline.append({
                "id": e.id,
                "type": "timeline_event",
                "event_type": e.event_type,
                "title": e.title,
                "description": e.description,
                "date": str(e.event_date) if e.event_date else str(e.created_at),
                "source": "investigation",
                "investigation_id": e.investigation_id,
            })

        for log in status_logs:
            timeline.append({
                "id": log.id,
                "type": "status_change",
                "event_type": "status",
                "title": f"Status: {log.old_status} → {log.new_status}",
                "description": log.notes,
                "date": str(log.changed_at) if log.changed_at else None,
                "source": "case_status",
                "investigation_id": log.investigation_id,
            })

        timeline.sort(key=lambda x: x.get("date") or "", reverse=True)

        # Group by date
        grouped = defaultdict(list)
        for item in timeline:
            date_key = (item.get("date") or "")[:10]
            grouped[date_key].append(item)

        return {
            "events": timeline,
            "grouped": dict(grouped),
            "total": len(timeline),
            "days": days,
        }

    async def get_suspect_timeline(self, suspect_name: str, days: int = 90) -> dict:
        date_from = datetime.utcnow() - timedelta(days=days)

        stmt = select(TimelineEvent).where(
            TimelineEvent.created_at >= date_from,
            or_(
                TimelineEvent.title.ilike(f"%{suspect_name}%"),
                TimelineEvent.description.ilike(f"%{suspect_name}%"),
            )
        ).order_by(TimelineEvent.event_date.desc().nullslast())
        result = await self.db.execute(stmt)
        events = result.scalars().all()

        timeline = [
            {
                "id": e.id,
                "event_type": e.event_type,
                "title": e.title,
                "description": e.description,
                "date": str(e.event_date) if e.event_date else str(e.created_at),
                "investigation_id": e.investigation_id,
            }
            for e in events
        ]

        return {"suspect": suspect_name, "events": timeline, "total": len(timeline)}

    async def get_investigation_timeline(self, investigation_id: int) -> dict:
        stmt = select(TimelineEvent).where(
            TimelineEvent.investigation_id == investigation_id
        ).order_by(TimelineEvent.event_date.desc().nullslast())
        result = await self.db.execute(stmt)
        events = result.scalars().all()

        timeline = [
            {
                "id": e.id,
                "event_type": e.event_type,
                "title": e.title,
                "description": e.description,
                "date": str(e.event_date) if e.event_date else str(e.created_at),
            }
            for e in events
        ]

        return {"investigation_id": investigation_id, "events": timeline, "total": len(timeline)}

    async def get_event_stats(self) -> dict:
        total = (await self.db.execute(select(sql_func.count(TimelineEvent.id)))).scalar() or 0
        by_type = {}
        stmt = select(TimelineEvent.event_type, sql_func.count(TimelineEvent.id)).group_by(TimelineEvent.event_type)
        result = await self.db.execute(stmt)
        for row in result.all():
            by_type[row[0]] = row[1]

        investigations = (await self.db.execute(
            select(sql_func.count(sql_func.distinct(TimelineEvent.investigation_id)))
        )).scalar() or 0

        return {"total_events": total, "by_type": by_type, "investigations_with_timeline": investigations}
