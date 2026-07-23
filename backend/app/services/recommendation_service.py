import json
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func, or_
from app.models.case import Case
from app.models.crime import Crime
from app.models.investigation import Investigation
from app.models.suspect import Suspect
from app.models.evidence import Evidence
from app.models.case_similarity import CaseSimilarity
from app.models.case_priority import CasePriority
from app.models.officer_intel import Recommendation, RecommendationHistory
from app.models.case_link import CaseLink
import structlog

logger = structlog.get_logger()

SIMILAR_WEIGHT = 0.30
MO_WEIGHT = 0.25
LOCATION_WEIGHT = 0.20
TEMPORAL_WEIGHT = 0.15
CROSS_DISTRICT_WEIGHT = 0.10


class RecommendationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_recommendations(self, rec_type: str = None, status: str = "active", limit: int = 20) -> dict:
        stmt = select(Recommendation).where(Recommendation.status == status)
        if rec_type:
            stmt = stmt.where(Recommendation.rec_type == rec_type)
        stmt = stmt.order_by(Recommendation.score.desc()).limit(limit)
        result = await self.db.execute(stmt)
        recs = result.scalars().all()
        return {
            "recommendations": [self._rec_to_dict(r) for r in recs],
            "total_count": len(recs),
        }

    async def generate_and_persist(self, context_type: str = "dashboard", entity_id: int = None) -> dict:
        if context_type == "case" and entity_id:
            result = await self.get_case_recommendations(entity_id)
        elif context_type == "investigation" and entity_id:
            result = await self.get_investigation_recommendations(entity_id)
        else:
            result = await self.get_dashboard_recommendations()

        recs = result.get("recommendations", [])
        persisted = 0
        for rec in recs:
            exists_stmt = select(Recommendation).where(
                Recommendation.rec_type == rec.get("type", ""),
                Recommendation.entity_type == self._infer_entity_type(rec),
                Recommendation.entity_id == self._infer_entity_id(rec),
                Recommendation.status == "active",
            )
            exists_result = await self.db.execute(exists_stmt)
            if exists_result.scalar():
                continue

            new_rec = Recommendation(
                rec_type=rec.get("type", ""),
                entity_type=self._infer_entity_type(rec),
                entity_id=self._infer_entity_id(rec),
                title=rec.get("title") or rec.get("name") or rec.get("message", ""),
                description=rec.get("description", ""),
                score=rec.get("score", 0),
                reasons_json=json.dumps(rec.get("reasons", [])),
                status="active",
                metadata_json=json.dumps({k: v for k, v in rec.items() if k not in ("type", "title", "name", "score", "reasons", "description", "message")}),
                confidence=rec.get("score", 0) / 100.0,
                recommendation=rec.get("title") or rec.get("name") or "",
            )
            self.db.add(new_rec)
            persisted += 1

            history = RecommendationHistory(
                recommendation_id=0,
                action="created",
                new_status="active",
            )
            self.db.add(history)

        if persisted > 0:
            await self.db.commit()

        result["persisted"] = persisted
        return result

    async def provide_feedback(self, recommendation_id: int, feedback: str) -> dict:
        stmt = select(Recommendation).where(Recommendation.id == recommendation_id)
        result = await self.db.execute(stmt)
        rec = result.scalar()
        if not rec:
            return {"error": "Recommendation not found"}

        old_status = rec.status
        if feedback == "accepted":
            rec.status = "accepted"
        elif feedback == "dismissed":
            rec.status = "dismissed"
        rec.feedback = feedback

        history = RecommendationHistory(
            recommendation_id=recommendation_id,
            action="rated",
            old_status=old_status,
            new_status=rec.status,
            metadata_json=json.dumps({"feedback": feedback}),
        )
        self.db.add(history)
        await self.db.commit()
        return self._rec_to_dict(rec)

    async def dismiss_recommendation(self, recommendation_id: int) -> dict:
        stmt = select(Recommendation).where(Recommendation.id == recommendation_id)
        result = await self.db.execute(stmt)
        rec = result.scalar()
        if not rec:
            return {"error": "Recommendation not found"}

        old_status = rec.status
        rec.status = "dismissed"

        history = RecommendationHistory(
            recommendation_id=recommendation_id,
            action="dismissed",
            old_status=old_status,
            new_status="dismissed",
        )
        self.db.add(history)
        await self.db.commit()
        return self._rec_to_dict(rec)

    async def get_recommendation_history(self, recommendation_id: int = None, limit: int = 50) -> dict:
        stmt = select(RecommendationHistory)
        if recommendation_id:
            stmt = stmt.where(RecommendationHistory.recommendation_id == recommendation_id)
        stmt = stmt.order_by(RecommendationHistory.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        history = result.scalars().all()
        return {
            "history": [
                {
                    "id": h.id,
                    "recommendation_id": h.recommendation_id,
                    "action": h.action,
                    "old_status": h.old_status,
                    "new_status": h.new_status,
                    "metadata": json.loads(h.metadata_json) if h.metadata_json else None,
                    "created_at": h.created_at.isoformat() if h.created_at else None,
                }
                for h in history
            ],
            "total_count": len(history),
        }

    async def get_dashboard_recommendations(self) -> dict:
        similar_recs = await self._get_similar_case_recommendations(limit=3)
        suspect_recs = await self._get_suspect_recommendations(limit=2)
        cross_district = await self._get_cross_district_recommendations(limit=2)
        evidence_recs = await self._get_evidence_review_recommendations(limit=2)
        priority_recs = await self._get_priority_escalation_recommendations(limit=2)
        officer_recs = await self._get_officer_assignment_recommendations(limit=1)
        related_inv = await self._get_related_investigation_recommendations(limit=2)

        all_recs = similar_recs + suspect_recs + cross_district + evidence_recs + priority_recs + officer_recs + related_inv
        all_recs.sort(key=lambda x: x.get("score", 0), reverse=True)
        active_investigations = await self._get_active_investigations(limit=3)

        return {
            "recommendations": all_recs[:10],
            "active_investigations": active_investigations,
            "total_count": len(all_recs),
        }

    async def get_case_recommendations(self, case_id: int) -> dict:
        similar = await self._get_similar_for_case(case_id, limit=5)
        case = await self._load_case(case_id)
        mo_recs = []
        evidence_recs = []
        if case:
            mo_recs = await self._get_mo_pattern_recommendations(case, limit=3)
            evidence_recs = await self._get_evidence_review_recommendations(limit=2)

        all_recs = similar + mo_recs + evidence_recs
        all_recs.sort(key=lambda x: x.get("score", 0), reverse=True)
        return {"case_id": case_id, "recommendations": all_recs[:7], "total_count": len(all_recs)}

    async def get_investigation_recommendations(self, investigation_id: int) -> dict:
        stmt = select(Investigation).where(Investigation.id == investigation_id)
        result = await self.db.execute(stmt)
        inv = result.scalar()
        if not inv:
            return {"investigation_id": investigation_id, "recommendations": [], "total_count": 0}

        similar = await self._get_similar_for_case(inv.case_id or 0, limit=3) if inv.case_id else []
        suspect_recs = await self._get_suspect_recommendations(limit=2)
        related_inv = await self._get_related_investigation_recommendations(limit=2)
        priority_recs = await self._get_priority_escalation_recommendations(limit=2)

        all_recs = similar + suspect_recs + related_inv + priority_recs
        all_recs.sort(key=lambda x: x.get("score", 0), reverse=True)
        return {"investigation_id": investigation_id, "recommendations": all_recs[:7], "total_count": len(all_recs)}

    async def natural_language_search(self, query: str) -> dict:
        results = []
        stmt = select(Case).where(
            or_(
                Case.title.ilike(f"%{query}%"),
                Case.description.ilike(f"%{query}%"),
                Case.crime_type.ilike(f"%{query}%"),
                Case.district.ilike(f"%{query}%"),
            )
        ).limit(10)
        db_result = await self.db.execute(stmt)
        cases = db_result.scalars().all()
        for case in cases:
            results.append({
                "type": "case", "id": case.id, "title": case.title,
                "crime_type": case.crime_type, "district": case.district,
                "status": case.status, "relevance": self._calculate_relevance(query, case),
            })

        stmt2 = select(Suspect).where(
            or_(
                Suspect.name.ilike(f"%{query}%"),
                Suspect.district.ilike(f"%{query}%"),
                Suspect.description.ilike(f"%{query}%"),
            )
        ).limit(5)
        db_result2 = await self.db.execute(stmt2)
        suspects = db_result2.scalars().all()
        for suspect in suspects:
            results.append({
                "type": "suspect", "id": suspect.id, "name": suspect.name,
                "district": suspect.district, "status": suspect.status,
                "risk_score": suspect.risk_score, "relevance": 50,
            })

        results.sort(key=lambda x: x.get("relevance", 0), reverse=True)
        return {"query": query, "results": results[:10], "total_count": len(results)}

    def _calculate_relevance(self, query: str, case) -> float:
        score = 0
        q = query.lower()
        if q in (case.title or "").lower():
            score += 40
        if q in (case.crime_type or "").lower():
            score += 30
        if q in (case.district or "").lower():
            score += 20
        if q in (case.description or "").lower():
            score += 10
        return min(100, score)

    async def _get_similar_case_recommendations(self, limit: int = 5) -> List[dict]:
        stmt = (
            select(CaseSimilarity)
            .where(CaseSimilarity.status == "active")
            .order_by(CaseSimilarity.overall_score.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        similarities = result.scalars().all()
        recs = []
        for sim in similarities:
            case = await self._load_case(sim.case_id_2)
            recs.append({
                "type": "similar_case", "case_id": sim.case_id_2,
                "linked_case_id": sim.case_id_1,
                "title": case.get("title", "") if case else "",
                "crime_type": case.get("crime_type", "") if case else "",
                "district": case.get("district", "") if case else "",
                "score": round(sim.overall_score, 1),
                "reasons": self._parse_reasons(sim.reasons_json),
                "dimensions": {"mo": round(sim.mo_score, 1), "location": round(sim.location_score, 1), "time": round(sim.time_score, 1)},
            })
        return recs

    async def _get_suspect_recommendations(self, limit: int = 2) -> List[dict]:
        stmt = select(Suspect).where(Suspect.risk_score > 0.5).order_by(Suspect.risk_score.desc()).limit(limit)
        result = await self.db.execute(stmt)
        suspects = result.scalars().all()
        return [
            {
                "type": "suspect_alert", "suspect_id": s.id, "name": s.name,
                "district": s.district, "risk_score": round(s.risk_score * 100, 1),
                "status": s.status, "description": (s.description or "")[:150],
                "score": round(s.risk_score * 100, 1),
            }
            for s in suspects
        ]

    async def _get_cross_district_recommendations(self, limit: int = 2) -> List[dict]:
        stmt = (
            select(Case.district, sql_func.count(Case.id).label("count"))
            .where(Case.status == "open")
            .group_by(Case.district)
            .having(sql_func.count(Case.id) > 1)
            .order_by(sql_func.count(Case.id).desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        rows = result.all()
        return [
            {
                "type": "cross_district", "district": row[0], "case_count": row[1],
                "score": min(80, row[1] * 15),
                "message": f"{row[1]} open cases in {row[0]} — potential pattern",
            }
            for row in rows
        ]

    async def _get_evidence_review_recommendations(self, limit: int = 5) -> List[dict]:
        try:
            stmt = (
                select(Evidence)
                .join(Case, Evidence.case_id == Case.id)
                .where(Case.status == "open")
                .order_by(Evidence.created_at.asc())
                .limit(limit)
            )
            result = await self.db.execute(stmt)
            evidence_items = result.scalars().all()
            recs = []
            for ev in evidence_items:
                case = await self._load_case(ev.case_id)
                recs.append({
                    "type": "evidence_review",
                    "evidence_id": ev.id,
                    "case_id": ev.case_id,
                    "title": f"Evidence #{ev.id} needs review",
                    "description": f"Linked to case: {case.get('title', 'Unknown') if case else 'Unknown'}",
                    "score": 65,
                    "reasons": ["Unreviewed evidence in open case", f"Case: {case.get('title', '') if case else ''}"],
                })
            return recs
        except Exception as e:
            logger.warning("evidence_review_error", error=str(e))
            return []

    async def _get_priority_escalation_recommendations(self, limit: int = 5) -> List[dict]:
        try:
            stmt = (
                select(CasePriority)
                .join(Case, CasePriority.case_id == Case.id)
                .where(Case.status == "open")
                .order_by(CasePriority.overall_score.desc())
                .limit(limit)
            )
            result = await self.db.execute(stmt)
            priorities = result.scalars().all()
            recs = []
            for p in priorities:
                if p.overall_score < 60:
                    continue
                case = await self._load_case(p.case_id)
                recs.append({
                    "type": "priority_escalation",
                    "case_id": p.case_id,
                    "title": f"Priority escalation: {case.get('title', 'Case') if case else 'Case'}",
                    "description": f"Priority score {p.overall_score:.0f} — needs immediate attention",
                    "score": round(p.overall_score, 1),
                    "reasons": [f"Priority score: {p.overall_score:.0f}/100"],
                })
            return recs
        except Exception as e:
            logger.warning("priority_escalation_error", error=str(e))
            return []

    async def _get_officer_assignment_recommendations(self, limit: int = 3) -> List[dict]:
        try:
            stmt = (
                select(Case)
                .where(Case.status == "open")
                .order_by(Case.created_at.asc())
                .limit(limit)
            )
            result = await self.db.execute(stmt)
            cases = result.scalars().all()
            recs = []
            for c in cases:
                recs.append({
                    "type": "officer_assignment",
                    "case_id": c.id,
                    "title": f"Assign officer to: {c.title}",
                    "description": f"Open case in {c.district} without assigned officer",
                    "score": 55,
                    "reasons": [f"Unassigned case in {c.district}", f"Type: {c.crime_type}"],
                })
            return recs
        except Exception as e:
            logger.warning("officer_assignment_error", error=str(e))
            return []

    async def _get_related_investigation_recommendations(self, limit: int = 3) -> List[dict]:
        try:
            stmt = select(CaseLink).limit(20)
            result = await self.db.execute(stmt)
            links = result.scalars().all()
            if not links:
                return []

            seen = set()
            recs = []
            for link in links:
                key = (link.case_id_1, link.case_id_2)
                if key in seen:
                    continue
                seen.add(key)

                case1 = await self._load_case(link.case_id_1)
                case2 = await self._load_case(link.case_id_2)
                if not case1 or not case2:
                    continue

                reasons = []
                score = 40
                if case1.get("crime_type") == case2.get("crime_type"):
                    reasons.append(f"Same crime type: {case1['crime_type']}")
                    score += 25
                if case1.get("district") == case2.get("district"):
                    reasons.append(f"Same district: {case1['district']}")
                    score += 20

                recs.append({
                    "type": "related_investigation",
                    "case_id": link.case_id_2,
                    "title": f"Related: {case2.get('title', 'Case')} ↔ {case1.get('title', 'Case')}",
                    "description": f"Linked cases sharing connections",
                    "score": min(95, score),
                    "reasons": reasons or ["Linked by case relationship"],
                })

            recs.sort(key=lambda x: x["score"], reverse=True)
            return recs[:limit]
        except Exception as e:
            logger.warning("related_investigation_error", error=str(e))
            return []

    async def _get_active_investigations(self, limit: int = 3) -> List[dict]:
        stmt = (
            select(Investigation)
            .where(Investigation.status == "active")
            .order_by(Investigation.progress.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        investigations = result.scalars().all()
        return [
            {"id": inv.id, "title": inv.title, "status": inv.status, "progress": inv.progress, "district": inv.district}
            for inv in investigations
        ]

    async def _get_similar_for_case(self, case_id: int, limit: int = 5) -> List[dict]:
        if not case_id:
            return []
        stmt = (
            select(CaseSimilarity)
            .where(
                or_(CaseSimilarity.case_id_1 == case_id, CaseSimilarity.case_id_2 == case_id),
                CaseSimilarity.status == "active",
            )
            .order_by(CaseSimilarity.overall_score.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        similarities = result.scalars().all()
        recs = []
        for sim in similarities:
            other_id = sim.case_id_2 if sim.case_id_1 == case_id else sim.case_id_1
            case = await self._load_case(other_id)
            recs.append({
                "type": "similar_case", "case_id": other_id,
                "title": case.get("title", "") if case else "",
                "crime_type": case.get("crime_type", "") if case else "",
                "score": round(sim.overall_score, 1),
                "reasons": self._parse_reasons(sim.reasons_json),
            })
        return recs

    async def _get_mo_pattern_recommendations(self, case: dict, limit: int = 3) -> List[dict]:
        crime_type = case.get("crime_type", "")
        if not crime_type:
            return []
        stmt = (
            select(Case)
            .where(Case.crime_type == crime_type, Case.id != case.get("id"))
            .order_by(Case.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        cases = result.scalars().all()
        return [
            {
                "type": "mo_pattern", "case_id": c.id, "title": c.title,
                "crime_type": c.crime_type, "district": c.district, "score": 60,
                "reasons": [f"Same crime type: {crime_type}"],
            }
            for c in cases
        ]

    async def _load_case(self, case_id: int) -> Optional[dict]:
        stmt = select(Case).where(Case.id == case_id)
        result = await self.db.execute(stmt)
        case = result.scalar()
        if not case:
            return None
        return {"id": case.id, "title": case.title, "crime_type": case.crime_type, "district": case.district, "status": case.status,
                "crime_no": case.crime_no, "case_category_id": case.case_category_id, "gravity_offence_id": case.gravity_offence_id,
                "police_station_id": case.police_station_id}

    def _parse_reasons(self, reasons_json: str) -> List[str]:
        if not reasons_json:
            return []
        try:
            return json.loads(reasons_json)
        except Exception:
            return []

    def _infer_entity_type(self, rec: dict) -> str:
        if rec.get("case_id"):
            return "case"
        if rec.get("suspect_id"):
            return "suspect"
        if rec.get("evidence_id"):
            return "evidence"
        if rec.get("district"):
            return "district"
        return "unknown"

    def _infer_entity_id(self, rec: dict) -> int:
        return rec.get("case_id") or rec.get("suspect_id") or rec.get("evidence_id") or 0

    def _rec_to_dict(self, rec: Recommendation) -> dict:
        return {
            "id": rec.id,
            "rec_type": rec.rec_type,
            "entity_type": rec.entity_type,
            "entity_id": rec.entity_id,
            "title": rec.title or rec.recommendation or "",
            "description": rec.description or "",
            "score": rec.score or rec.confidence or 0,
            "reasons": self._parse_reasons(rec.reasons_json),
            "status": rec.status,
            "feedback": rec.feedback,
            "metadata": json.loads(rec.metadata_json) if rec.metadata_json else None,
            "created_at": rec.created_at.isoformat() if rec.created_at else None,
        }
