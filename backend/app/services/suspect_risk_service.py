import json
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.suspect import Suspect
from app.models.criminal import Criminal
from app.models.suspect_risk_score import SuspectRiskScore
from app.models.risk_score_history import RiskScoreHistory
from app.models.risk_factor import RiskFactor
import structlog
from datetime import datetime

logger = structlog.get_logger()

WEIGHTS = {
    "criminal_history": 0.15,
    "offense_severity": 0.15,
    "age_factor": 0.08,
    "location_risk": 0.12,
    "associate_risk": 0.12,
    "recency": 0.12,
    "network_influence": 0.10,
    "mo_similarity": 0.08,
    "investigation_links": 0.05,
    "behavioral": 0.03,
}


class SuspectRiskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def score_suspect(self, suspect_id: int) -> dict:
        suspect = await self._load_suspect(suspect_id)
        if not suspect:
            return {"error": "Suspect not found"}

        criminal = await self._load_criminal(suspect_id)

        # Calculate individual scores
        scores = {}
        try:
            scores["criminal_history"] = self._score_criminal_history(criminal)
            scores["offense_severity"] = self._score_offense_severity(criminal)
            scores["age_factor"] = self._score_age(suspect)
            scores["location_risk"] = self._score_location(suspect)
            scores["associate_risk"] = self._score_associates(criminal)
            scores["recency"] = self._score_recency(criminal)
            scores["network_influence"] = self._score_network(suspect)
            scores["mo_similarity"] = self._score_mo(criminal)
            scores["investigation_links"] = self._score_investigation(suspect)
            scores["behavioral"] = self._score_behavioral(criminal)
        except Exception as e:
            logger.warning("score_calculation_error", suspect_id=suspect_id, error=str(e))
            scores = {k: 20.0 for k in WEIGHTS}

        overall = sum(scores[k] * WEIGHTS[k] for k in scores)
        risk_level = "very_high" if overall >= 75 else "high" if overall >= 50 else "medium" if overall >= 25 else "low"

        # Build explanation
        explanation = []
        for factor, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            if score > 50:
                explanation.append(f"{factor.replace('_', ' ').title()}: {score:.0f}% contribution")

        evidence = []
        if criminal:
            if criminal.mo_description:
                evidence.append({"factor": "MO", "detail": criminal.mo_description[:200]})
            if criminal.behavioral_profile:
                evidence.append({"factor": "Behavioral", "detail": criminal.behavioral_profile[:200]})

        # Save score
        existing = await self._score_exists(suspect_id)
        if existing:
            existing.overall_score = round(overall, 1)
            existing.risk_level = risk_level
            for k, v in scores.items():
                col = f"{k}_score"
                if hasattr(existing, col):
                    setattr(existing, col, round(v, 1))
            existing.explanation_json = json.dumps(explanation)
            existing.evidence_json = json.dumps(evidence)
            existing.scored_at = datetime.utcnow()
            score_id = existing.id
        else:
            risk_score = SuspectRiskScore(
                suspect_id=suspect_id,
                overall_score=round(overall, 1),
                risk_level=risk_level,
                criminal_history_score=round(scores["criminal_history"], 1),
                offense_severity_score=round(scores["offense_severity"], 1),
                age_factor_score=round(scores["age_factor"], 1),
                location_risk_score=round(scores["location_risk"], 1),
                associate_risk_score=round(scores["associate_risk"], 1),
                recency_score=round(scores["recency"], 1),
                network_influence_score=round(scores["network_influence"], 1),
                mo_similarity_score=round(scores["mo_similarity"], 1),
                investigation_links_score=round(scores["investigation_links"], 1),
                behavioral_score=round(scores["behavioral"], 1),
                explanation_json=json.dumps(explanation),
                evidence_json=json.dumps(evidence),
            )
            self.db.add(risk_score)
            await self.db.flush()
            score_id = risk_score.id

        # Save history
        history = RiskScoreHistory(
            suspect_id=suspect_id,
            score=round(overall, 1),
            risk_level=risk_level,
        )
        self.db.add(history)

        # Save factors
        for factor_name, factor_score in scores.items():
            rf = RiskFactor(
                suspect_id=suspect_id,
                factor_name=factor_name,
                factor_value=round(factor_score, 1),
                weight=WEIGHTS.get(factor_name, 0),
                description=f"{factor_name.replace('_', ' ').title()} contribution: {factor_score:.0f}%",
                source="risk_engine",
            )
            self.db.add(rf)

        # Update suspect risk_score
        try:
            suspect.risk_score = round(overall / 100, 2)
        except Exception:
            pass
        await self.db.commit()

        return {
            "suspect_id": suspect_id,
            "name": suspect.name,
            "overall_score": round(overall, 1),
            "risk_level": risk_level,
            "scores": {k: round(v, 1) for k, v in scores.items()},
            "explanation": explanation,
            "evidence": evidence,
        }

    async def get_scores(self, suspect_id: int = None) -> List[dict]:
        stmt = select(SuspectRiskScore)
        if suspect_id:
            stmt = stmt.where(SuspectRiskScore.suspect_id == suspect_id)
        stmt = stmt.order_by(SuspectRiskScore.overall_score.desc())
        result = await self.db.execute(stmt)
        return [self._score_to_dict(s) for s in result.scalars().all()]

    async def get_history(self, suspect_id: int) -> List[dict]:
        stmt = select(RiskScoreHistory).where(
            RiskScoreHistory.suspect_id == suspect_id
        ).order_by(RiskScoreHistory.scored_at.desc())
        result = await self.db.execute(stmt)
        return [
            {"score": h.score, "risk_level": h.risk_level, "scored_at": str(h.scored_at) if h.scored_at else None,
             "change": h.change_from_previous}
            for h in result.scalars().all()
        ]

    async def get_factors(self, suspect_id: int) -> List[dict]:
        stmt = select(RiskFactor).where(RiskFactor.suspect_id == suspect_id)
        result = await self.db.execute(stmt)
        return [
            {"name": f.factor_name, "value": f.factor_value, "weight": f.weight,
             "description": f.description, "source": f.source}
            for f in result.scalars().all()
        ]

    async def get_rankings(self, limit: int = 10) -> List[dict]:
        stmt = select(SuspectRiskScore).order_by(SuspectRiskScore.overall_score.desc()).limit(limit)
        result = await self.db.execute(stmt)
        scores = result.scalars().all()
        rankings = []
        for s in scores:
            suspect = await self._load_suspect(s.suspect_id)
            rankings.append({
                "suspect_id": s.suspect_id,
                "name": suspect.get("name", "Unknown") if suspect else "Unknown",
                "overall_score": s.overall_score,
                "risk_level": s.risk_level,
                "district": suspect.get("district", "") if suspect else "",
            })
        return rankings

    async def batch_score(self) -> dict:
        stmt = select(Suspect)
        result = await self.db.execute(stmt)
        suspects = result.scalars().all()
        scored = 0
        errors = 0
        for suspect in suspects:
            try:
                await self.score_suspect(suspect.id)
                scored += 1
            except Exception as e:
                logger.warning("batch_score_error", suspect_id=suspect.id, error=str(e))
                errors += 1
                await self.db.rollback()
        return {"suspects_scored": scored, "errors": errors}

    async def get_stats(self) -> dict:
        total = (await self.db.execute(select(sql_func.count(SuspectRiskScore.id)))).scalar() or 0
        high = (await self.db.execute(
            select(sql_func.count(SuspectRiskScore.id)).where(SuspectRiskScore.risk_level.in_(["high", "very_high"]))
        )).scalar() or 0
        avg = (await self.db.execute(select(sql_func.avg(SuspectRiskScore.overall_score)))).scalar()
        return {"total_scored": total, "high_risk": high, "avg_score": round(avg or 0, 1)}

    async def _load_suspect(self, suspect_id: int) -> Optional[dict]:
        stmt = select(Suspect).where(Suspect.id == suspect_id)
        result = await self.db.execute(stmt)
        s = result.scalar()
        return {"id": s.id, "name": s.name, "age": s.age, "gender": s.gender,
                "district": s.district, "status": s.status, "risk_score": s.risk_score,
                "description": s.description} if s else None

    async def _load_criminal(self, suspect_id: int) -> Optional[dict]:
        stmt = select(Criminal).where(Criminal.person_id == suspect_id)
        result = await self.db.execute(stmt)
        c = result.scalar()
        return {"id": c.id, "alias": c.alias, "risk_score": c.risk_score,
                "mo_description": c.mo_description, "behavioral_profile": c.behavioral_profile,
                "first_offense_date": c.first_offense_date} if c else None

    def _score_criminal_history(self, criminal) -> float:
        if not criminal:
            return 10
        return min(100, (criminal.get("risk_score", 0) or 0) * 100)

    def _score_offense_severity(self, criminal) -> float:
        if not criminal:
            return 30
        mo = (criminal.get("mo_description") or "").lower()
        if any(w in mo for w in ["murder", "kill", "homicide"]):
            return 90
        if any(w in mo for w in ["robbery", "armed", "weapon"]):
            return 70
        if any(w in mo for w in ["assault", "attack", "violence"]):
            return 55
        return 35

    def _score_age(self, suspect) -> float:
        age = suspect.get("age") or 30
        if age < 25:
            return 75
        if age < 35:
            return 55
        if age < 50:
            return 35
        return 20

    def _score_location(self, suspect) -> float:
        district = (suspect.get("district") or "").lower()
        high_risk = ["bengaluru", "mysuru", "mangaluru"]
        return 70 if any(hr in district for hr in high_risk) else 30

    def _score_associates(self, criminal) -> float:
        if not criminal:
            return 20
        return min(100, (criminal.get("risk_score", 0) or 0) * 80)

    def _score_recency(self, criminal) -> float:
        if not criminal:
            return 30
        first_offense = criminal.get("first_offense_date")
        if not first_offense:
            return 40
        try:
            from datetime import datetime
            offense_date = datetime.strptime(first_offense, "%Y-%m-%d")
            years_ago = (datetime.now() - offense_date).days / 365
            return max(10, min(100, 100 - years_ago * 10))
        except Exception:
            return 40

    def _score_network(self, suspect) -> float:
        desc = (suspect.get("description") or "").lower()
        if any(w in desc for w in ["gang", "network", "organized", "group"]):
            return 80
        if any(w in desc for w in ["associate", "connected", "linked"]):
            return 50
        return 25

    def _score_mo(self, criminal) -> float:
        if not criminal:
            return 20
        mo = (criminal.get("mo_description") or "").lower()
        if len(mo) > 100:
            return 70
        if len(mo) > 50:
            return 50
        return 25

    def _score_investigation(self, suspect) -> float:
        desc = (suspect.get("description") or "").lower()
        if any(w in desc for w in ["investigation", "suspect", "wanted", "linked"]):
            return 70
        return 20

    def _score_behavioral(self, criminal) -> float:
        if not criminal:
            return 20
        bp = (criminal.get("behavioral_profile") or "").lower()
        if len(bp) > 100:
            return 65
        if len(bp) > 50:
            return 45
        return 20

    async def _score_exists(self, suspect_id: int) -> Optional[SuspectRiskScore]:
        stmt = select(SuspectRiskScore).where(SuspectRiskScore.suspect_id == suspect_id)
        result = await self.db.execute(stmt)
        return result.scalar()

    def _score_to_dict(self, s: SuspectRiskScore) -> dict:
        return {
            "id": s.id, "suspect_id": s.suspect_id,
            "overall_score": s.overall_score, "risk_level": s.risk_level,
            "explanation": json.loads(s.explanation_json) if s.explanation_json else [],
            "scored_at": str(s.scored_at) if s.scored_at else None,
        }
