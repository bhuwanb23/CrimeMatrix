from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, union_all, desc
from app.models.intelligence_event import IntelligenceEvent
from app.models.processed_event import ProcessedEvent
from app.models.alert_event import AlertEvent
from app.models.early_warning_alert import EarlyWarningAlert
from app.models.evidence_link import EvidenceLink
from app.models.link_history_record import LinkHistoryRecord
from app.models.match_history_record import MatchHistoryRecord
from app.models.cross_district_match import CrossDistrictMatch
from app.models.officer_intel import RecommendationHistory
from app.models.risk_score_history import RiskScoreHistory
from app.models.priority_history_record import PriorityHistoryRecord
import structlog

logger = structlog.get_logger()


class IntelligenceTimelineService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_unified_timeline(
        self, limit: int = 50, offset: int = 0,
        source: str = None, entity_type: str = None,
    ) -> dict:
        entries = []

        if not source or source == "event":
            entries += await self._get_event_entries(limit + offset + 50)
        if not source or source == "alert":
            entries += await self._get_alert_entries(limit + offset + 50)
        if not source or source == "evidence":
            entries += await self._get_evidence_entries(limit + offset + 50)
        if not source or source == "recommendation":
            entries += await self._get_recommendation_entries(limit + offset + 50)
        if not source or source == "risk":
            entries += await self._get_risk_entries(limit + offset + 50)
        if not source or source == "match":
            entries += await self._get_match_entries(limit + offset + 50)

        if entity_type:
            entries = [e for e in entries if e.get("entity_type") == entity_type]

        entries.sort(key=lambda x: x.get("created_at") or "", reverse=True)
        total = len(entries)
        entries = entries[offset:offset + limit]

        return {
            "entries": entries,
            "total_count": total,
            "limit": limit,
            "offset": offset,
        }

    async def get_event_history(self, limit: int = 30) -> dict:
        entries = await self._get_event_entries(limit)
        return {"entries": entries, "total_count": len(entries)}

    async def get_alert_history(self, limit: int = 30) -> dict:
        entries = await self._get_alert_entries(limit)
        return {"entries": entries, "total_count": len(entries)}

    async def get_evidence_history(self, limit: int = 30) -> dict:
        entries = await self._get_evidence_entries(limit)
        return {"entries": entries, "total_count": len(entries)}

    async def get_recommendation_history(self, limit: int = 30) -> dict:
        entries = await self._get_recommendation_entries(limit)
        return {"entries": entries, "total_count": len(entries)}

    async def get_risk_history(self, limit: int = 30) -> dict:
        entries = await self._get_risk_entries(limit)
        return {"entries": entries, "total_count": len(entries)}

    async def get_timeline_stats(self) -> dict:
        stats = {}
        for label, query_fn in [
            ("events", self._count_table(IntelligenceEvent)),
            ("processed", self._count_table(ProcessedEvent)),
            ("alerts", self._count_table(AlertEvent)),
            ("early_warnings", self._count_table(EarlyWarningAlert)),
            ("evidence_links", self._count_table(EvidenceLink)),
            ("link_history", self._count_table(LinkHistoryRecord)),
            ("match_history", self._count_table(MatchHistoryRecord)),
            ("cross_district", self._count_table(CrossDistrictMatch)),
            ("recommendation_history", self._count_table(RecommendationHistory)),
            ("risk_history", self._count_table(RiskScoreHistory)),
            ("priority_history", self._count_table(PriorityHistoryRecord)),
        ]:
            try:
                stats[label] = await query_fn
            except Exception:
                stats[label] = 0

        stats["total_timeline"] = sum(stats.values())
        return stats

    def _count_table(self, model):
        async def _count():
            from sqlalchemy import func as sql_func
            stmt = select(sql_func.count()).select_from(model)
            result = await self.db.execute(stmt)
            return result.scalar() or 0
        return _count()

    async def _get_event_entries(self, limit: int) -> List[dict]:
        stmt = (
            select(IntelligenceEvent)
            .order_by(desc(IntelligenceEvent.created_at))
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        events = result.scalars().all()
        entries = []
        for e in events:
            entries.append({
                "id": f"event_{e.id}",
                "source": "event",
                "source_id": e.id,
                "action": e.status or "created",
                "entity_type": e.entity_type or "unknown",
                "entity_id": e.entity_id,
                "title": f"{(e.event_type or 'Event').replace('_', ' ').title()}" + (f" — {e.entity_type} #{e.entity_id}" if e.entity_id else ""),
                "details": e.event_data or "",
                "score": None,
                "created_at": e.created_at.isoformat() if e.created_at else None,
            })
        return entries

    async def _get_alert_entries(self, limit: int) -> List[dict]:
        entries = []

        stmt = (
            select(EarlyWarningAlert)
            .order_by(desc(EarlyWarningAlert.created_at))
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        for a in result.scalars().all():
            entries.append({
                "id": f"alert_{a.id}",
                "source": "alert",
                "source_id": a.id,
                "action": a.status or "detected",
                "entity_type": "case" if a.case_id else "system",
                "entity_id": a.case_id,
                "title": f"{(a.alert_type or 'Alert').replace('_', ' ').title()} — {a.title}",
                "details": (a.description or "")[:200],
                "score": a.confidence * 100 if a.confidence else None,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            })

        stmt2 = (
            select(AlertEvent)
            .order_by(desc(AlertEvent.created_at))
            .limit(limit)
        )
        result2 = await self.db.execute(stmt2)
        for ae in result2.scalars().all():
            entries.append({
                "id": f"alert_event_{ae.id}",
                "source": "alert",
                "source_id": ae.id,
                "action": ae.event_type or "updated",
                "entity_type": "alert",
                "entity_id": ae.alert_id,
                "title": f"Alert #{ae.alert_id} — {(ae.event_type or 'event').replace('_', ' ').title()}",
                "details": ae.message or "",
                "score": None,
                "created_at": ae.created_at.isoformat() if ae.created_at else None,
            })
        return entries

    async def _get_evidence_entries(self, limit: int) -> List[dict]:
        entries = []

        stmt = (
            select(EvidenceLink)
            .order_by(desc(EvidenceLink.created_at))
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        for el in result.scalars().all():
            entries.append({
                "id": f"elink_{el.id}",
                "source": "evidence",
                "source_id": el.id,
                "action": "detected",
                "entity_type": "evidence",
                "entity_id": el.evidence_id_1,
                "title": f"Evidence #{el.evidence_id_1} → #{el.evidence_id_2} — {(el.link_type or 'link').replace('_', ' ').title()}",
                "details": el.link_reason or "",
                "score": el.confidence,
                "created_at": el.created_at.isoformat() if el.created_at else None,
            })

        stmt2 = (
            select(LinkHistoryRecord)
            .order_by(desc(LinkHistoryRecord.created_at))
            .limit(limit)
        )
        result2 = await self.db.execute(stmt2)
        for lh in result2.scalars().all():
            entries.append({
                "id": f"lhist_{lh.id}",
                "source": "evidence",
                "source_id": lh.id,
                "action": lh.action or "updated",
                "entity_type": "evidence_link",
                "entity_id": lh.link_id,
                "title": f"Link #{lh.link_id} — {(lh.action or 'updated').title()}",
                "details": "",
                "score": None,
                "created_at": lh.created_at.isoformat() if lh.created_at else None,
            })
        return entries

    async def _get_recommendation_entries(self, limit: int) -> List[dict]:
        stmt = (
            select(RecommendationHistory)
            .order_by(desc(RecommendationHistory.created_at))
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        entries = []
        for rh in result.scalars().all():
            entries.append({
                "id": f"rec_{rh.id}",
                "source": "recommendation",
                "source_id": rh.id,
                "action": rh.action or "created",
                "entity_type": "recommendation",
                "entity_id": rh.recommendation_id,
                "title": f"Recommendation #{rh.recommendation_id} — {(rh.action or 'created').title()}",
                "details": f"Status: {rh.old_status or '?'} → {rh.new_status or '?'}" if rh.new_status else "",
                "score": None,
                "created_at": rh.created_at.isoformat() if rh.created_at else None,
            })
        return entries

    async def _get_risk_entries(self, limit: int) -> List[dict]:
        entries = []

        stmt = (
            select(RiskScoreHistory)
            .order_by(desc(RiskScoreHistory.scored_at))
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        for rh in result.scalars().all():
            entries.append({
                "id": f"risk_{rh.id}",
                "source": "risk",
                "source_id": rh.id,
                "action": "scored",
                "entity_type": "suspect",
                "entity_id": rh.suspect_id,
                "title": f"Suspect #{rh.suspect_id} — Risk: {rh.risk_level or '?'} ({rh.score:.0f}%)",
                "details": f"Change: {rh.change_from_previous:+.1f}%" if rh.change_from_previous else "",
                "score": rh.score,
                "created_at": rh.scored_at.isoformat() if rh.scored_at else None,
            })

        stmt2 = (
            select(PriorityHistoryRecord)
            .order_by(desc(PriorityHistoryRecord.scored_at))
            .limit(limit)
        )
        result2 = await self.db.execute(stmt2)
        for ph in result2.scalars().all():
            entries.append({
                "id": f"prio_{ph.id}",
                "source": "risk",
                "source_id": ph.id,
                "action": "scored",
                "entity_type": "investigation",
                "entity_id": ph.investigation_id,
                "title": f"Investigation #{ph.investigation_id} — Priority: {ph.priority_level or '?'} ({ph.priority_score:.0f})",
                "details": f"Change: {ph.change_from_previous:+.1f}%" if ph.change_from_previous else "",
                "score": ph.priority_score,
                "created_at": ph.scored_at.isoformat() if ph.scored_at else None,
            })
        return entries

    async def _get_match_entries(self, limit: int) -> List[dict]:
        entries = []

        stmt = (
            select(CrossDistrictMatch)
            .order_by(desc(CrossDistrictMatch.created_at))
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        for cm in result.scalars().all():
            entries.append({
                "id": f"match_{cm.id}",
                "source": "match",
                "source_id": cm.id,
                "action": "detected",
                "entity_type": cm.entity_type or "suspect",
                "entity_id": cm.entity_id,
                "title": f"Cross-district: {cm.district_1} ↔ {cm.district_2} — {(cm.match_type or '?').title()}",
                "details": cm.match_reason or "",
                "score": cm.confidence,
                "created_at": cm.created_at.isoformat() if cm.created_at else None,
            })

        stmt2 = (
            select(MatchHistoryRecord)
            .order_by(desc(MatchHistoryRecord.created_at))
            .limit(limit)
        )
        result2 = await self.db.execute(stmt2)
        for mh in result2.scalars().all():
            entries.append({
                "id": f"mhist_{mh.id}",
                "source": "match",
                "source_id": mh.id,
                "action": mh.action or "updated",
                "entity_type": "match",
                "entity_id": mh.match_id,
                "title": f"Match #{mh.match_id} — {(mh.action or 'updated').title()}",
                "details": "",
                "score": None,
                "created_at": mh.created_at.isoformat() if mh.created_at else None,
            })
        return entries
