import json
import math
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from app.models.case import Case
from app.models.crime import Crime
from app.models.suspect import Suspect
from app.models.evidence import Evidence
from app.models.vehicle import Vehicle
from app.models.case_embedding import CaseEmbedding
from app.models.case_similarity import CaseSimilarity
import structlog

logger = structlog.get_logger()

# Weights for multi-factor scoring
DIMENSION_WEIGHTS = {
    "mo": 0.30,
    "location": 0.20,
    "time": 0.10,
    "suspects": 0.15,
    "evidence": 0.15,
    "vehicles": 0.10,
}


class SimilarCaseService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_similar(self, case_id: int, top_k: int = 10) -> List[dict]:
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
            .limit(top_k)
        )
        result = await self.db.execute(stmt)
        rows = result.scalars().all()

        similar = []
        for row in rows:
            other_id = row.case_id_2 if row.case_id_1 == case_id else row.case_id_1
            case = await self._load_case(other_id)
            reasons = json.loads(row.reasons_json) if row.reasons_json else []
            entry = {
                "case_id": other_id,
                "overall_score": round(row.overall_score, 1),
                "mo_score": round(row.mo_score, 1),
                "location_score": round(row.location_score, 1),
                "time_score": round(row.time_score, 1),
                "suspects_score": round(row.suspects_score, 1),
                "evidence_score": round(row.evidence_score, 1),
                "vehicles_score": round(row.vehicles_score, 1),
                "reasons": reasons,
            }
            if case:
                entry.update({
                    "case_number": case.get("case_number", ""),
                    "title": case.get("title", ""),
                    "crime_type": case.get("crime_type", ""),
                    "district": case.get("district", ""),
                    "status": case.get("status", ""),
                })
            similar.append(entry)

        return similar

    async def compute_similarity(self, case_id: int = None, force: bool = False) -> dict:
        if case_id:
            cases = [case_id]
        else:
            stmt = select(Case.id)
            result = await self.db.execute(stmt)
            cases = [r[0] for r in result.fetchall()]

        computed = 0
        skipped = 0
        for cid in cases:
            if not force:
                existing = await self._has_similarity(cid)
                if existing:
                    skipped += 1
                    continue

            profile = await self._build_case_profile(cid)
            if not profile:
                continue

            other_ids = [o for o in cases if o != cid]
            for other_id in other_ids:
                other_profile = await self._build_case_profile(other_id)
                if not other_profile:
                    continue

                scores = self._compute_all_dimensions(profile, other_profile)
                overall = sum(scores[d] * w for d, w in DIMENSION_WEIGHTS.items())
                reasons = self._get_reasons(profile, other_profile, scores)

                await self._save_similarity(
                    cid, other_id, overall, scores, reasons
                )
                computed += 1

        return {"computed": computed, "skipped": skipped, "total_cases": len(cases)}

    async def compare_cases(self, id1: int, id2: int) -> dict:
        profile1 = await self._build_case_profile(id1)
        profile2 = await self._build_case_profile(id2)

        if not profile1 or not profile2:
            return {"error": "One or both cases not found"}

        scores = self._compute_all_dimensions(profile1, profile2)
        overall = sum(scores[d] * w for d, w in DIMENSION_WEIGHTS.items())
        reasons = self._get_reasons(profile1, profile2, scores)

        dimension_details = {}
        for dim, score in scores.items():
            dimension_details[dim] = {
                "score": round(score, 1),
                "weight": DIMENSION_WEIGHTS[dim],
                "weighted": round(score * DIMENSION_WEIGHTS[dim], 1),
                "detail": self._get_dimension_detail(dim, profile1, profile2),
            }

        return {
            "case_1": profile1,
            "case_2": profile2,
            "dimension_scores": dimension_details,
            "overall_score": round(overall, 1),
            "reasons": reasons,
        }

    async def _build_case_profile(self, case_id: int) -> Optional[dict]:
        case = await self._load_case(case_id)
        if not case:
            return None

        suspects = await self._load_suspects(case_id)
        evidence = await self._load_evidence(case_id)
        vehicles = await self._load_vehicles(case_id)

        return {
            "id": case_id,
            "case_number": case.get("case_number", ""),
            "title": case.get("title", ""),
            "description": case.get("description", ""),
            "crime_type": case.get("crime_type", ""),
            "district": case.get("district", ""),
            "status": case.get("status", ""),
            "priority": case.get("priority", ""),
            "created_at": case.get("created_at"),
            "suspects": suspects,
            "evidence": evidence,
            "vehicles": vehicles,
        }

    def _compute_all_dimensions(self, p1: dict, p2: dict) -> dict:
        return {
            "mo": self._score_mo(p1, p2),
            "location": self._score_location(p1, p2),
            "time": self._score_time(p1, p2),
            "suspects": self._score_suspects(p1, p2),
            "evidence": self._score_evidence(p1, p2),
            "vehicles": self._score_vehicles(p1, p2),
        }

    def _score_mo(self, p1: dict, p2: dict) -> float:
        text1 = f"{p1.get('title', '')} {p1.get('description', '')} {p1.get('crime_type', '')}".lower()
        text2 = f"{p2.get('title', '')} {p2.get('description', '')} {p2.get('crime_type', '')}".lower()

        if not text1.strip() or not text2.strip():
            return 0

        words1 = set(text1.split())
        words2 = set(text2.split())
        stopwords = {"the", "and", "was", "for", "that", "with", "they", "from", "have", "this", "were", "been", "said", "a", "an", "is", "in", "on", "at", "to", "of", "by"}
        words1 -= stopwords
        words2 -= stopwords

        if not words1 or not words2:
            return 0

        overlap = len(words1 & words2)
        union = len(words1 | words2)
        jaccard = overlap / union if union else 0

        type_match = 1.0 if p1.get("crime_type", "").lower() == p2.get("crime_type", "").lower() else 0

        return min(100, (jaccard * 60 + type_match * 40))

    def _score_location(self, p1: dict, p2: dict) -> float:
        d1 = p1.get("district", "").lower().strip()
        d2 = p2.get("district", "").lower().strip()

        if not d1 or not d2:
            return 0
        if d1 == d2:
            return 100
        return 0

    def _score_time(self, p1: dict, p2: dict) -> float:
        t1 = p1.get("created_at")
        t2 = p2.get("created_at")

        if not t1 or not t2:
            return 0

        if isinstance(t1, str):
            try:
                t1 = datetime.fromisoformat(t1.replace("Z", "+00:00"))
            except Exception:
                return 0
        if isinstance(t2, str):
            try:
                t2 = datetime.fromisoformat(t2.replace("Z", "+00:00"))
            except Exception:
                return 0

        diff = abs((t1 - t2).total_seconds())
        days = diff / 86400

        if days <= 7:
            return 90
        elif days <= 30:
            return 75
        elif days <= 90:
            return 60
        elif days <= 365:
            return 40
        else:
            return 20

    def _score_suspects(self, p1: dict, p2: dict) -> float:
        s1 = p1.get("suspects", [])
        s2 = p2.get("suspects", [])

        if not s1 or not s2:
            return 0

        names1 = {s.get("name", "").lower() for s in s1 if s.get("name")}
        names2 = {s.get("name", "").lower() for s in s2 if s.get("name")}
        name_overlap = len(names1 & names2) / max(len(names1 | names2), 1) if names1 or names2 else 0

        districts1 = {s.get("district", "").lower() for s in s1 if s.get("district")}
        districts2 = {s.get("district", "").lower() for s in s2 if s.get("district")}
        dist_overlap = len(districts1 & districts2) / max(len(districts1 | districts2), 1) if districts1 or districts2 else 0

        return min(100, (name_overlap * 60 + dist_overlap * 40))

    def _score_evidence(self, p1: dict, p2: dict) -> float:
        e1 = p1.get("evidence", [])
        e2 = p2.get("evidence", [])

        if not e1 or not e2:
            return 0

        types1 = {e.get("evidence_type", "").lower() for e in e1 if e.get("evidence_type")}
        types2 = {e.get("evidence_type", "").lower() for e in e2 if e.get("evidence_type")}
        type_overlap = len(types1 & types2) / max(len(types1 | types2), 1) if types1 or types2 else 0

        descs1 = " ".join(e.get("description", "") for e in e1 if e.get("description")).lower().split()
        descs2 = " ".join(e.get("description", "") for e in e2 if e.get("description")).lower().split()
        words1 = set(descs1) - {"the", "and", "was", "for", "that", "with"}
        words2 = set(descs2) - {"the", "and", "was", "for", "that", "with"}
        desc_overlap = len(words1 & words2) / max(len(words1 | words2), 1) if words1 or words2 else 0

        return min(100, (type_overlap * 50 + desc_overlap * 50))

    def _score_vehicles(self, p1: dict, p2: dict) -> float:
        v1 = p1.get("vehicles", [])
        v2 = p2.get("vehicles", [])

        if not v1 or not v2:
            return 0

        score = 0
        for va in v1:
            for vb in v2:
                match_score = 0
                if va.get("make", "").lower() == vb.get("make", "").lower():
                    match_score += 30
                if va.get("model", "").lower() == vb.get("model", "").lower():
                    match_score += 25
                if va.get("color", "").lower() == vb.get("color", "").lower():
                    match_score += 20
                if va.get("type", "").lower() == vb.get("type", "").lower():
                    match_score += 25
                score = max(score, match_score)

        return min(100, score)

    def _get_reasons(self, p1: dict, p2: dict, scores: dict) -> List[str]:
        reasons = []
        if scores["mo"] > 50:
            if p1.get("crime_type", "").lower() == p2.get("crime_type", "").lower():
                reasons.append(f"Same crime type: {p1.get('crime_type')}")
        if scores["location"] >= 80:
            reasons.append(f"Same district: {p1.get('district')}")
        if scores["time"] >= 75:
            reasons.append("Occurred within same month")
        elif scores["time"] >= 40:
            reasons.append("Occurred within same year")
        if scores["suspects"] > 30:
            s1_names = {s.get("name", "") for s in p1.get("suspects", []) if s.get("name")}
            s2_names = {s.get("name", "") for s in p2.get("suspects", []) if s.get("name")}
            shared = s1_names & s2_names
            if shared:
                reasons.append(f"Shared suspect: {', '.join(shared)}")
        if scores["evidence"] > 40:
            e1_types = {e.get("evidence_type", "") for e in p1.get("evidence", []) if e.get("evidence_type")}
            e2_types = {e.get("evidence_type", "") for e in p2.get("evidence", []) if e.get("evidence_type")}
            shared = e1_types & e2_types
            if shared:
                reasons.append(f"Shared evidence type: {', '.join(shared)}")
        if scores["vehicles"] > 30:
            reasons.append("Similar vehicle involvement")
        return reasons

    def _get_dimension_detail(self, dim: str, p1: dict, p2: dict) -> str:
        if dim == "mo":
            ct1, ct2 = p1.get("crime_type", ""), p2.get("crime_type", "")
            if ct1.lower() == ct2.lower():
                return f"Both are {ct1}"
            return f"Types: {ct1} vs {ct2}"
        elif dim == "location":
            d1, d2 = p1.get("district", ""), p2.get("district", "")
            return f"Same district: {d1}" if d1.lower() == d2.lower() else f"Districts: {d1} vs {d2}"
        elif dim == "time":
            return "Temporal proximity analysis"
        elif dim == "suspects":
            s1 = len(p1.get("suspects", []))
            s2 = len(p2.get("suspects", []))
            return f"Suspects: {s1} vs {s2}"
        elif dim == "evidence":
            e1 = len(p1.get("evidence", []))
            e2 = len(p2.get("evidence", []))
            return f"Evidence items: {e1} vs {e2}"
        elif dim == "vehicles":
            v1 = len(p1.get("vehicles", []))
            v2 = len(p2.get("vehicles", []))
            return f"Vehicles: {v1} vs {v2}"
        return ""

    async def _has_similarity(self, case_id: int) -> bool:
        stmt = select(CaseSimilarity).where(
            or_(
                CaseSimilarity.case_id_1 == case_id,
                CaseSimilarity.case_id_2 == case_id,
            )
        ).limit(1)
        result = await self.db.execute(stmt)
        return result.scalar() is not None

    async def _save_similarity(self, id1: int, id2: int, overall: float, scores: dict, reasons: List[str]):
        c1, c2 = (min(id1, id2), max(id1, id2))
        stmt = select(CaseSimilarity).where(
            CaseSimilarity.case_id_1 == c1,
            CaseSimilarity.case_id_2 == c2,
        )
        result = await self.db.execute(stmt)
        existing = result.scalar()

        if existing:
            existing.overall_score = overall
            existing.mo_score = scores["mo"]
            existing.location_score = scores["location"]
            existing.time_score = scores["time"]
            existing.suspects_score = scores["suspects"]
            existing.evidence_score = scores["evidence"]
            existing.vehicles_score = scores["vehicles"]
            existing.reasons_json = json.dumps(reasons)
        else:
            row = CaseSimilarity(
                case_id_1=c1,
                case_id_2=c2,
                overall_score=overall,
                mo_score=scores["mo"],
                location_score=scores["location"],
                time_score=scores["time"],
                suspects_score=scores["suspects"],
                evidence_score=scores["evidence"],
                vehicles_score=scores["vehicles"],
                reasons_json=json.dumps(reasons),
            )
            self.db.add(row)

        await self.db.commit()

    async def _load_case(self, case_id: int) -> Optional[dict]:
        stmt = select(Case).where(Case.id == case_id)
        result = await self.db.execute(stmt)
        case = result.scalar()
        if not case:
            return None
        return {
            "id": case.id,
            "case_number": case.case_number,
            "title": case.title,
            "description": case.description,
            "crime_type": case.crime_type,
            "district": case.district,
            "status": case.status,
            "priority": case.priority,
            "created_at": str(case.created_at) if case.created_at else None,
        }

    async def _load_suspects(self, case_id: int) -> List[dict]:
        stmt = select(Suspect).where(Suspect.id.isnot(None)).limit(20)
        result = await self.db.execute(stmt)
        suspects = result.scalars().all()
        return [
            {"id": s.id, "name": s.name, "age": s.age, "district": s.district, "status": s.status, "description": s.description}
            for s in suspects
        ]

    async def _load_evidence(self, case_id: int) -> List[dict]:
        stmt = select(Evidence).where(Evidence.case_id == case_id)
        result = await self.db.execute(stmt)
        items = result.scalars().all()
        return [
            {"id": e.id, "evidence_type": e.evidence_type, "description": e.description, "status": e.status}
            for e in items
        ]

    async def _load_vehicles(self, case_id: int) -> List[dict]:
        stmt = select(Vehicle).limit(20)
        result = await self.db.execute(stmt)
        vehicles = result.scalars().all()
        return [
            {"id": v.id, "registration_number": v.registration_number, "make": v.make, "model": v.model, "color": v.color, "type": v.type}
            for v in vehicles
        ]

    async def get_stats(self) -> dict:
        from sqlalchemy import func as sql_func
        count_stmt = select(sql_func.count(CaseSimilarity.id))
        result = await self.db.execute(count_stmt)
        total_pairs = result.scalar() or 0

        avg_stmt = select(sql_func.avg(CaseSimilarity.overall_score))
        result = await self.db.execute(avg_stmt)
        avg_score = result.scalar() or 0

        embed_stmt = select(sql_func.count(CaseEmbedding.id))
        result = await self.db.execute(embed_stmt)
        total_embeddings = result.scalar() or 0

        return {
            "total_similarity_pairs": total_pairs,
            "average_score": round(avg_score, 1),
            "total_embeddings": total_embeddings,
        }
