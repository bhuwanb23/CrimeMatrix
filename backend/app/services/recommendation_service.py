from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func, or_
from app.models.case import Case
from app.models.crime import Crime
from app.models.investigation import Investigation
from app.models.suspect import Suspect
from app.models.case_similarity import CaseSimilarity
import structlog

logger = structlog.get_logger()

# Weights for recommendation scoring
SIMILAR_WEIGHT = 0.30
MO_WEIGHT = 0.25
LOCATION_WEIGHT = 0.20
TEMPORAL_WEIGHT = 0.15
CROSS_DISTRICT_WEIGHT = 0.10


class RecommendationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dashboard_recommendations(self) -> dict:
        similar_recs = await self._get_similar_case_recommendations(limit=3)
        suspect_recs = await self._get_suspect_recommendations(limit=2)
        cross_district = await self._get_cross_district_recommendations(limit=2)
        active_investigations = await self._get_active_investigations(limit=3)

        all_recs = similar_recs + suspect_recs + cross_district
        all_recs.sort(key=lambda x: x.get("score", 0), reverse=True)

        return {
            "recommendations": all_recs[:7],
            "active_investigations": active_investigations,
            "total_count": len(all_recs),
        }

    async def get_case_recommendations(self, case_id: int) -> dict:
        similar = await self._get_similar_for_case(case_id, limit=5)
        case = await self._load_case(case_id)

        mo_recs = []
        if case:
            mo_recs = await self._get_mo_pattern_recommendations(case, limit=3)

        all_recs = similar + mo_recs
        all_recs.sort(key=lambda x: x.get("score", 0), reverse=True)

        return {
            "case_id": case_id,
            "recommendations": all_recs[:5],
            "total_count": len(all_recs),
        }

    async def get_investigation_recommendations(self, investigation_id: int) -> dict:
        stmt = select(Investigation).where(Investigation.id == investigation_id)
        result = await self.db.execute(stmt)
        inv = result.scalar()
        if not inv:
            return {"investigation_id": investigation_id, "recommendations": [], "total_count": 0}

        similar = await self._get_similar_for_case(inv.case_id or 0, limit=3) if inv.case_id else []
        suspect_recs = await self._get_suspect_recommendations(limit=2)

        all_recs = similar + suspect_recs
        all_recs.sort(key=lambda x: x.get("score", 0), reverse=True)

        return {
            "investigation_id": investigation_id,
            "recommendations": all_recs[:5],
            "total_count": len(all_recs),
        }

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
                "type": "case",
                "id": case.id,
                "title": case.title,
                "crime_type": case.crime_type,
                "district": case.district,
                "status": case.status,
                "relevance": self._calculate_relevance(query, case),
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
                "type": "suspect",
                "id": suspect.id,
                "name": suspect.name,
                "district": suspect.district,
                "status": suspect.status,
                "risk_score": suspect.risk_score,
                "relevance": 50,
            })

        results.sort(key=lambda x: x.get("relevance", 0), reverse=True)

        return {
            "query": query,
            "results": results[:10],
            "total_count": len(results),
        }

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
                "type": "similar_case",
                "case_id": sim.case_id_2,
                "linked_case_id": sim.case_id_1,
                "title": case.get("title", "") if case else "",
                "crime_type": case.get("crime_type", "") if case else "",
                "district": case.get("district", "") if case else "",
                "score": round(sim.overall_score, 1),
                "reasons": self._parse_reasons(sim.reasons_json),
                "dimensions": {
                    "mo": round(sim.mo_score, 1),
                    "location": round(sim.location_score, 1),
                    "time": round(sim.time_score, 1),
                },
            })
        return recs

    async def _get_suspect_recommendations(self, limit: int = 2) -> List[dict]:
        stmt = (
            select(Suspect)
            .where(Suspect.risk_score > 0.5)
            .order_by(Suspect.risk_score.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        suspects = result.scalars().all()

        return [
            {
                "type": "suspect_alert",
                "suspect_id": s.id,
                "name": s.name,
                "district": s.district,
                "risk_score": round(s.risk_score * 100, 1),
                "status": s.status,
                "description": (s.description or "")[:150],
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

        recs = []
        for row in rows:
            recs.append({
                "type": "cross_district",
                "district": row[0],
                "case_count": row[1],
                "score": min(80, row[1] * 15),
                "message": f"{row[1]} open cases in {row[0]} — potential pattern",
            })
        return recs

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
            {
                "id": inv.id,
                "title": inv.title,
                "status": inv.status,
                "progress": inv.progress,
                "district": inv.district,
            }
            for inv in investigations
        ]

    async def _get_similar_for_case(self, case_id: int, limit: int = 5) -> List[dict]:
        if not case_id:
            return []
        stmt = (
            select(CaseSimilarity)
            .where(
                or_(
                    CaseSimilarity.case_id_1 == case_id,
                    CaseSimilarity.case_id_2 == case_id,
                ),
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
                "type": "similar_case",
                "case_id": other_id,
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
                "type": "mo_pattern",
                "case_id": c.id,
                "title": c.title,
                "crime_type": c.crime_type,
                "district": c.district,
                "score": 60,
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
        return {
            "id": case.id,
            "title": case.title,
            "crime_type": case.crime_type,
            "district": case.district,
            "status": case.status,
        }

    def _parse_reasons(self, reasons_json: str) -> List[str]:
        if not reasons_json:
            return []
        try:
            import json
            return json.loads(reasons_json)
        except Exception:
            return []
