from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.investigation import Investigation
from app.models.note import Note
from app.models.timeline_event import TimelineEvent
from app.models.evidence import Evidence
from app.models.attachment import Attachment
from app.models.case_link import CaseLink
from app.models.case_status_log import CaseStatusLog
import structlog

logger = structlog.get_logger()


class InvestigationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_investigations(
        self, status: str = None, search: str = None, limit: int = 50, offset: int = 0
    ) -> List[dict]:
        stmt = select(Investigation)
        if status:
            stmt = stmt.where(Investigation.status == status)
        if search:
            stmt = stmt.where(Investigation.title.ilike(f"%{search}%"))
        stmt = stmt.order_by(Investigation.created_at.desc()).offset(offset).limit(limit)

        result = await self.db.execute(stmt)
        investigations = result.scalars().all()

        items = []
        for inv in investigations:
            counts = await self._get_counts(inv.id)
            items.append({
                "id": inv.id,
                "case_id": inv.case_id,
                "title": inv.title,
                "status": inv.status,
                "priority": inv.priority,
                "progress": inv.progress,
                "district": inv.district,
                "officer_id": inv.officer_id,
                "created_at": str(inv.created_at) if inv.created_at else None,
                "updated_at": str(inv.updated_at) if inv.updated_at else None,
                **counts,
            })
        return items

    async def get_investigation(self, investigation_id: int) -> Optional[dict]:
        stmt = select(Investigation).where(Investigation.id == investigation_id)
        result = await self.db.execute(stmt)
        inv = result.scalar()
        if not inv:
            return None

        notes = await self._get_notes(investigation_id)
        evidence = await self._get_evidence(inv.case_id)
        timeline = await self._get_timeline(investigation_id)
        case_links = await self._get_case_links(investigation_id)
        status_logs = await self._get_status_logs(investigation_id)
        attachments = await self._get_attachments(investigation_id)

        return {
            "id": inv.id,
            "case_id": inv.case_id,
            "title": inv.title,
            "description": inv.description,
            "status": inv.status,
            "priority": inv.priority,
            "progress": inv.progress,
            "district": inv.district,
            "officer_id": inv.officer_id,
            "created_at": str(inv.created_at) if inv.created_at else None,
            "updated_at": str(inv.updated_at) if inv.updated_at else None,
            "notes": notes,
            "evidence": evidence,
            "timeline": timeline,
            "case_links": case_links,
            "status_logs": status_logs,
            "attachments": attachments,
        }

    async def create_investigation(self, data: Dict[str, Any]) -> dict:
        inv = Investigation(**data)
        self.db.add(inv)
        await self.db.commit()
        await self.db.refresh(inv)
        return {
            "id": inv.id,
            "case_id": inv.case_id,
            "title": inv.title,
            "description": inv.description,
            "status": inv.status,
            "priority": inv.priority,
            "progress": inv.progress,
            "district": inv.district,
            "officer_id": inv.officer_id,
            "created_at": str(inv.created_at) if inv.created_at else None,
        }

    async def update_investigation(self, investigation_id: int, data: Dict[str, Any]) -> Optional[dict]:
        stmt = select(Investigation).where(Investigation.id == investigation_id)
        result = await self.db.execute(stmt)
        inv = result.scalar()
        if not inv:
            return None

        for key, value in data.items():
            if value is not None and hasattr(inv, key):
                setattr(inv, key, value)

        await self.db.commit()
        await self.db.refresh(inv)
        return {
            "id": inv.id,
            "case_id": inv.case_id,
            "title": inv.title,
            "status": inv.status,
            "priority": inv.priority,
            "progress": inv.progress,
            "district": inv.district,
        }

    async def delete_investigation(self, investigation_id: int) -> bool:
        stmt = select(Investigation).where(Investigation.id == investigation_id)
        result = await self.db.execute(stmt)
        inv = result.scalar()
        if not inv:
            return False
        await self.db.delete(inv)
        await self.db.commit()
        return True

    async def _get_counts(self, investigation_id: int) -> dict:
        notes_count = await self._count(Note, Note.investigation_id == investigation_id)
        timeline_count = await self._count(TimelineEvent, TimelineEvent.investigation_id == investigation_id)
        return {"notes_count": notes_count, "timeline_count": timeline_count}

    async def _count(self, model, condition):
        stmt = select(sql_func.count(model.id)).where(condition)
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def _get_notes(self, investigation_id: int) -> List[dict]:
        stmt = select(Note).where(Note.investigation_id == investigation_id).order_by(Note.created_at.desc())
        result = await self.db.execute(stmt)
        notes = result.scalars().all()
        return [
            {"id": n.id, "content": n.content, "author_id": n.author_id,
             "created_at": str(n.created_at) if n.created_at else None}
            for n in notes
        ]

    async def _get_evidence(self, case_id: int) -> List[dict]:
        if not case_id:
            return []
        stmt = select(Evidence).where(Evidence.case_id == case_id)
        result = await self.db.execute(stmt)
        items = result.scalars().all()
        return [
            {"id": e.id, "evidence_type": e.evidence_type, "description": e.description,
             "status": e.status, "file_path": e.file_path}
            for e in items
        ]

    async def _get_timeline(self, investigation_id: int) -> List[dict]:
        stmt = select(TimelineEvent).where(TimelineEvent.investigation_id == investigation_id).order_by(TimelineEvent.event_date.desc())
        result = await self.db.execute(stmt)
        events = result.scalars().all()
        return [
            {"id": e.id, "title": e.title, "description": e.description,
             "event_type": e.event_type, "event_date": str(e.event_date) if e.event_date else None,
             "created_at": str(e.created_at) if e.created_at else None}
            for e in events
        ]

    async def _get_case_links(self, investigation_id: int) -> List[dict]:
        stmt = select(CaseLink).where(CaseLink.investigation_id == investigation_id)
        result = await self.db.execute(stmt)
        links = result.scalars().all()
        return [
            {"id": l.id, "linked_case_id": l.linked_case_id, "link_type": l.link_type,
             "description": l.description, "created_at": str(l.created_at) if l.created_at else None}
            for l in links
        ]

    async def _get_status_logs(self, investigation_id: int) -> List[dict]:
        stmt = select(CaseStatusLog).where(CaseStatusLog.investigation_id == investigation_id).order_by(CaseStatusLog.changed_at.desc())
        result = await self.db.execute(stmt)
        logs = result.scalars().all()
        return [
            {"id": l.id, "old_status": l.old_status, "new_status": l.new_status,
             "changed_by": l.changed_by, "notes": l.notes,
             "changed_at": str(l.changed_at) if l.changed_at else None}
            for l in logs
        ]

    async def _get_attachments(self, investigation_id: int) -> List[dict]:
        stmt = select(Attachment).where(Attachment.investigation_id == investigation_id)
        result = await self.db.execute(stmt)
        items = result.scalars().all()
        return [
            {"id": a.id, "filename": a.filename, "file_path": a.file_path,
             "file_size": a.file_size, "file_type": a.file_type,
             "uploaded_by": a.uploaded_by,
             "created_at": str(a.created_at) if a.created_at else None}
            for a in items
        ]
