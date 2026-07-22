import json
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.evidence import Evidence
from app.models.evidence_link import EvidenceLink
from app.models.evidence_relationship import EvidenceRelationship
from app.models.link_history_record import LinkHistoryRecord
import structlog
from datetime import datetime

logger = structlog.get_logger()


class EvidenceLinkingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def detect_links(self) -> dict:
        stmt = select(Evidence)
        result = await self.db.execute(stmt)
        evidence = result.scalars().all()

        links_found = 0
        by_type = defaultdict(list)
        for e in evidence:
            if e.evidence_type:
                by_type[e.evidence_type].append(e)

        # Link evidence of same type
        for etype, group in by_type.items():
            if len(group) > 1:
                for i in range(len(group)):
                    for j in range(i + 1, len(group)):
                        if group[i].case_id != group[j].case_id:
                            link = EvidenceLink(
                                evidence_id_1=group[i].id,
                                evidence_id_2=group[j].id,
                                link_type="same_type",
                                confidence=70,
                                link_reason=f"Same evidence type: {etype}",
                            )
                            self.db.add(link)
                            links_found += 1

        # Link evidence with similar descriptions
        for i in range(len(evidence)):
            for j in range(i + 1, len(evidence)):
                if evidence[i].case_id != evidence[j].case_id:
                    desc1 = (evidence[i].description or "").lower()
                    desc2 = (evidence[j].description or "").lower()
                    words1 = set(desc1.split())
                    words2 = set(desc2.split())
                    overlap = len(words1 & words2) / max(len(words1 | words2), 1) * 100
                    if overlap > 30:
                        link = EvidenceLink(
                            evidence_id_1=evidence[i].id,
                            evidence_id_2=evidence[j].id,
                            link_type="description_match",
                            confidence=round(overlap, 1),
                            link_reason=f"Description overlap: {overlap:.0f}%",
                        )
                        self.db.add(link)
                        links_found += 1

        await self.db.commit()
        return {"links_found": links_found, "total_evidence": len(evidence)}

    async def get_links(self, link_type: str = None) -> List[dict]:
        stmt = select(EvidenceLink)
        if link_type:
            stmt = stmt.where(EvidenceLink.link_type == link_type)
        stmt = stmt.order_by(EvidenceLink.confidence.desc())
        result = await self.db.execute(stmt)
        return [self._link_to_dict(l) for l in result.scalars().all()]

    async def get_link(self, link_id: int) -> Optional[dict]:
        stmt = select(EvidenceLink).where(EvidenceLink.id == link_id)
        result = await self.db.execute(stmt)
        l = result.scalar()
        return self._link_to_dict(l) if l else None

    async def get_relationships(self) -> List[dict]:
        stmt = select(EvidenceRelationship).order_by(EvidenceRelationship.strength.desc())
        result = await self.db.execute(stmt)
        return [
            {"id": r.id, "evidence_id": r.evidence_id, "case_id_1": r.case_id_1,
             "case_id_2": r.case_id_2, "relationship_type": r.relationship_type,
             "strength": r.strength}
            for r in result.scalars().all()
        ]

    async def get_stats(self) -> dict:
        total = (await self.db.execute(select(sql_func.count(EvidenceLink.id)))).scalar() or 0
        relationships = (await self.db.execute(select(sql_func.count(EvidenceRelationship.id)))).scalar() or 0
        return {"total_links": total, "total_relationships": relationships}

    def _link_to_dict(self, l: EvidenceLink) -> dict:
        return {
            "id": l.id, "evidence_id_1": l.evidence_id_1, "evidence_id_2": l.evidence_id_2,
            "link_type": l.link_type, "confidence": l.confidence, "link_reason": l.link_reason,
            "status": l.status, "created_at": str(l.created_at) if l.created_at else None,
        }
