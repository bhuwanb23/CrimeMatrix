import json
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.investigation import Investigation
from app.models.case import Case
from app.models.suspect import Suspect
from app.models.evidence import Evidence
from app.models.case_priority import CasePriority
from app.models.priority_history_record import PriorityHistoryRecord
from app.models.priority_explanation import PriorityExplanation
import structlog
from datetime import datetime, timedelta

logger = structlog.get_logger()

WEIGHTS = {
    "severity": 0.20,
    "victim_vulnerability": 0.12,
    "evidence_availability": 0.12,
    "repeat_offender": 0.15,
    "active_threats": 0.15,
    "investigation_age": 0.10,
    "cross_district": 0.08,
    "officer_workload": 0.08,
}


class PriorityService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def score_investigation(self, investigation_id: int) -> dict:
        inv = await self._load_investigation(investigation_id)
        if not inv:
            return {"error": "Investigation not found"}

        scores = {}
        scores["severity"] = self._score_severity(inv)
        scores["victim_vulnerability"] = self._score_victim_vulnerability(inv)
        scores["evidence_availability"] = self._score_evidence(inv)
        scores["repeat_offender"] = self._score_repeat_offender(inv)
        scores["active_threats"] = self._score_active_threats(inv)
        scores["investigation_age"] = self._score_age(inv)
        scores["cross_district"] = self._score_cross_district(inv)
        scores["officer_workload"] = self._score_officer_workload(inv)

        overall = sum(scores[k] * WEIGHTS[k] for k in scores)
        priority_level = "critical" if overall >= 75 else "high" if overall >= 50 else "medium" if overall >= 25 else "low"

        explanations = []
        for factor, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            if score > 30:
                explanations.append({
                    "factor": factor.replace("_", " ").title(),
                    "score": round(score, 1),
                    "weight": WEIGHTS.get(factor, 0),
                    "explanation": self._get_explanation(factor, score, inv),
                })

        # Save priority
        existing = await self._priority_exists(investigation_id)
        if existing:
            existing.overall_priority_score = round(overall, 1)
            existing.priority_level = priority_level
            for k, v in scores.items():
                col = f"{k}_score"
                if hasattr(existing, col):
                    setattr(existing, col, round(v, 1))
            existing.explanation_json = json.dumps(explanations)
            existing.scored_at = datetime.utcnow()
        else:
            priority = CasePriority(
                investigation_id=investigation_id,
                overall_priority_score=round(overall, 1),
                priority_level=priority_level,
                severity_score=round(scores["severity"], 1),
                victim_vulnerability_score=round(scores["victim_vulnerability"], 1),
                evidence_availability_score=round(scores["evidence_availability"], 1),
                repeat_offender_score=round(scores["repeat_offender"], 1),
                active_threats_score=round(scores["active_threats"], 1),
                investigation_age_score=round(scores["investigation_age"], 1),
                cross_district_score=round(scores["cross_district"], 1),
                officer_workload_score=round(scores["officer_workload"], 1),
                explanation_json=json.dumps(explanations),
            )
            self.db.add(priority)

        # Save history
        history = PriorityHistoryRecord(
            investigation_id=investigation_id,
            priority_score=round(overall, 1),
            priority_level=priority_level,
        )
        self.db.add(history)

        # Save explanations
        for exp in explanations:
            pe = PriorityExplanation(
                investigation_id=investigation_id,
                factor_name=exp["factor"],
                factor_score=exp["score"],
                weight=exp["weight"],
                explanation=exp["explanation"],
            )
            self.db.add(pe)

        await self.db.commit()

        return {
            "investigation_id": investigation_id,
            "overall_score": round(overall, 1),
            "priority_level": priority_level,
            "scores": {k: round(v, 1) for k, v in scores.items()},
            "explanations": explanations,
        }

    async def get_priorities(self, investigation_id: int = None) -> List[dict]:
        stmt = select(CasePriority)
        if investigation_id:
            stmt = stmt.where(CasePriority.investigation_id == investigation_id)
        stmt = stmt.order_by(CasePriority.overall_priority_score.desc())
        result = await self.db.execute(stmt)
        return [self._priority_to_dict(p) for p in result.scalars().all()]

    async def get_explain(self, investigation_id: int) -> List[dict]:
        stmt = select(PriorityExplanation).where(
            PriorityExplanation.investigation_id == investigation_id
        ).order_by(PriorityExplanation.factor_score.desc())
        result = await self.db.execute(stmt)
        return [
            {"factor": e.factor_name, "score": e.factor_score, "weight": e.weight,
             "explanation": e.explanation}
            for e in result.scalars().all()
        ]

    async def get_rankings(self, limit: int = 10) -> List[dict]:
        stmt = select(CasePriority).order_by(CasePriority.overall_priority_score.desc()).limit(limit)
        result = await self.db.execute(stmt)
        priorities = result.scalars().all()
        rankings = []
        for p in priorities:
            inv = await self._load_investigation(p.investigation_id)
            rankings.append({
                "investigation_id": p.investigation_id,
                "title": inv.get("title", "Unknown") if inv else "Unknown",
                "overall_score": p.overall_priority_score,
                "priority_level": p.priority_level,
                "district": inv.get("district", "") if inv else "",
                "progress": inv.get("progress", 0) if inv else 0,
            })
        return rankings

    async def get_history(self, investigation_id: int) -> List[dict]:
        stmt = select(PriorityHistoryRecord).where(
            PriorityHistoryRecord.investigation_id == investigation_id
        ).order_by(PriorityHistoryRecord.scored_at.desc())
        result = await self.db.execute(stmt)
        return [
            {"score": h.priority_score, "level": h.priority_level,
             "scored_at": str(h.scored_at) if h.scored_at else None,
             "change": h.change_from_previous}
            for h in result.scalars().all()
        ]

    async def get_workload(self) -> List[dict]:
        stmt = select(Investigation).where(Investigation.status == "active")
        result = await self.db.execute(stmt)
        investigations = result.scalars().all()

        officer_workload = {}
        for inv in investigations:
            officer_id = inv.officer_id or 0
            if officer_id not in officer_workload:
                officer_workload[officer_id] = {"officer_id": officer_id, "count": 0, "high_priority": 0}
            officer_workload[officer_id]["count"] += 1
            if inv.priority in ("high", "critical"):
                officer_workload[officer_id]["high_priority"] += 1

        return list(officer_workload.values())

    async def get_stats(self) -> dict:
        total = (await self.db.execute(select(sql_func.count(CasePriority.id)))).scalar() or 0
        critical = (await self.db.execute(
            select(sql_func.count(CasePriority.id)).where(CasePriority.priority_level == "critical")
        )).scalar() or 0
        high = (await self.db.execute(
            select(sql_func.count(CasePriority.id)).where(CasePriority.priority_level == "high")
        )).scalar() or 0
        avg = (await self.db.execute(select(sql_func.avg(CasePriority.overall_priority_score)))).scalar()
        return {"total_scored": total, "critical": critical, "high": high, "avg_score": round(avg or 0, 1)}

    async def batch_score(self) -> dict:
        stmt = select(Investigation)
        result = await self.db.execute(stmt)
        investigations = result.scalars().all()
        scored = 0
        for inv in investigations:
            try:
                await self.score_investigation(inv.id)
                scored += 1
            except Exception as e:
                logger.warning("batch_score_error", investigation_id=inv.id, error=str(e))
        return {"investigations_scored": scored}

    async def _load_investigation(self, investigation_id: int) -> Optional[dict]:
        stmt = select(Investigation).where(Investigation.id == investigation_id)
        result = await self.db.execute(stmt)
        inv = result.scalar()
        return {
            "id": inv.id, "title": inv.title, "description": inv.description,
            "status": inv.status, "priority": inv.priority, "progress": inv.progress,
            "district": inv.district, "officer_id": inv.officer_id,
            "created_at": str(inv.created_at) if inv.created_at else None,
        } if inv else None

    def _score_severity(self, inv: dict) -> float:
        priority = (inv.get("priority") or "").lower()
        if priority == "critical":
            return 90
        if priority == "high":
            return 70
        if priority == "medium":
            return 45
        return 20

    def _score_victim_vulnerability(self, inv: dict) -> float:
        desc = (inv.get("description") or "").lower()
        if any(w in desc for w in ["child", "juvenile", "elderly", "vulnerable"]):
            return 85
        if any(w in desc for w in ["woman", "female"]):
            return 60
        return 30

    def _score_evidence(self, inv: dict) -> float:
        progress = inv.get("progress") or 0
        if progress < 20:
            return 80
        if progress < 50:
            return 50
        return 25

    def _score_repeat_offender(self, inv: dict) -> float:
        desc = (inv.get("description") or "").lower()
        if any(w in desc for w in ["repeat", "serial", "known offender", "prior"]):
            return 80
        return 20

    def _score_active_threats(self, inv: dict) -> float:
        desc = (inv.get("description") or "").lower()
        if any(w in desc for w in ["threat", "dangerous", "armed", "weapon", "violent"]):
            return 85
        return 25

    def _score_age(self, inv: dict) -> float:
        created = inv.get("created_at")
        if not created:
            return 30
        try:
            created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            days_old = (datetime.utcnow() - created_dt).days
            if days_old > 90:
                return 80
            if days_old > 30:
                return 50
            return 20
        except Exception:
            return 30

    def _score_cross_district(self, inv: dict) -> float:
        desc = (inv.get("description") or "").lower()
        if any(w in desc for w in ["cross-district", "multi-district", "serial"]):
            return 75
        return 15

    def _score_officer_workload(self, inv: dict) -> float:
        progress = inv.get("progress") or 0
        if progress < 30:
            return 60
        return 25

    def _get_explanation(self, factor: str, score: float, inv: dict) -> str:
        explanations = {
            "severity": f"Priority level is {inv.get('priority', 'medium')} — {'requires immediate attention' if score > 60 else 'standard priority'}",
            "victim_vulnerability": "Case involves vulnerable victims" if score > 50 else "Standard victim profile",
            "evidence_availability": f"Investigation at {inv.get('progress', 0)}% progress — {'evidence collection needed' if score > 50 else 'evidence being processed'}",
            "repeat_offender": "Suspect linked to repeat offenses" if score > 50 else "No repeat offender indicators",
            "active_threats": "Active threats detected in case description" if score > 50 else "No active threats",
            "investigation_age": "Investigation requires attention due to age" if score > 50 else "Investigation is recent",
            "cross_district": "Cross-district coordination needed" if score > 50 else "Single district case",
            "officer_workload": "Officer workload suggests need for support" if score > 50 else "Workload is manageable",
        }
        return explanations.get(factor, "No explanation available")

    async def _priority_exists(self, investigation_id: int) -> Optional[CasePriority]:
        stmt = select(CasePriority).where(CasePriority.investigation_id == investigation_id)
        result = await self.db.execute(stmt)
        return result.scalar()

    async def _load_investigation(self, investigation_id: int) -> Optional[dict]:
        stmt = select(Investigation).where(Investigation.id == investigation_id)
        result = await self.db.execute(stmt)
        inv = result.scalar()
        return {
            "id": inv.id, "title": inv.title, "description": inv.description,
            "status": inv.status, "priority": inv.priority, "progress": inv.progress,
            "district": inv.district, "officer_id": inv.officer_id,
            "created_at": str(inv.created_at) if inv.created_at else None,
        } if inv else None

    def _priority_to_dict(self, p: CasePriority) -> dict:
        return {
            "id": p.id, "investigation_id": p.investigation_id,
            "overall_score": p.overall_priority_score, "priority_level": p.priority_level,
            "explanations": json.loads(p.explanation_json) if p.explanation_json else [],
            "scored_at": str(p.scored_at) if p.scored_at else None,
        }