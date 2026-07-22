import json
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.fir import FIR
from app.models.crime import Crime
from app.models.suspect import Suspect
from app.models.fir_suggestion import FIRSuggestion
from app.models.fir_analysis_history_record import FIRAnalysisHistoryRecord
import structlog
from datetime import datetime

logger = structlog.get_logger()

MO_KEYWORDS = {
    "entry": ["break", "window", "door", "lock", "force", "pry", "drill"],
    "weapon": ["knife", "gun", "weapon", "threat", "force", "violence"],
    "target": ["jewelry", "cash", "electronics", "vehicle", "phone", "wallet"],
    "method": ["snatch", "grab", "con", "trick", "ambush", "distraction"],
}


class FIRAnalysisService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze_fir(self, fir_id: int) -> dict:
        fir = await self._load_fir(fir_id)
        if not fir:
            return {"error": "FIR not found"}

        text = f"{fir.get('title', '')} {fir.get('description', '')} {fir.get('crime_type', '')}".lower()

        suggestions = []

        # 1. Similar cases
        similar = await self._find_similar_crimes(fir)
        for s in similar:
            suggestions.append({
                "suggestion_type": "similar_case",
                "suggestion_text": f"Similar case: {s.get('title', '')} (Score: {s.get('score', 0)}%)",
                "confidence": s.get("score", 0),
                "entity_id": s.get("id"),
                "entity_type": "crime",
            })

        # 2. MO pattern matches
        mo_matches = self._find_mo_matches(text)
        for m in mo_matches:
            suggestions.append({
                "suggestion_type": "mo_match",
                "suggestion_text": f"MO pattern: {m}",
                "confidence": 75,
                "entity_type": "pattern",
            })

        # 3. Suspect links
        suspect_links = await self._find_suspect_links(text)
        for s in suspect_links:
            suggestions.append({
                "suggestion_type": "suspect",
                "suggestion_text": f"Potential suspect: {s.get('name', '')} — {s.get('description', '')[:100]}",
                "confidence": 60,
                "entity_id": s.get("id"),
                "entity_type": "suspect",
            })

        # Save suggestions
        for sug in suggestions:
            fs = FIRSuggestion(
                fir_id=fir_id,
                suggestion_type=sug["suggestion_type"],
                suggestion_text=sug["suggestion_text"],
                confidence=sug["confidence"],
                entity_id=sug.get("entity_id"),
                entity_type=sug.get("entity_type"),
            )
            self.db.add(fs)

        # Save analysis history
        history = FIRAnalysisHistoryRecord(
            fir_id=fir_id,
            analysis_type="auto",
            analysis_result=json.dumps({"suggestions_count": len(suggestions)}),
            model_used="keyword_analysis",
            processing_time_ms=0,
        )
        self.db.add(history)
        await self.db.commit()

        return {"fir_id": fir_id, "suggestions": suggestions, "count": len(suggestions)}

    async def get_suggestions(self, fir_id: int) -> List[dict]:
        stmt = select(FIRSuggestion).where(FIRSuggestion.fir_id == fir_id).order_by(FIRSuggestion.confidence.desc())
        result = await self.db.execute(stmt)
        return [
            {"id": s.id, "suggestion_type": s.suggestion_type, "suggestion_text": s.suggestion_text,
             "confidence": s.confidence, "entity_id": s.entity_id, "entity_type": s.entity_type,
             "status": s.status, "created_at": str(s.created_at) if s.created_at else None}
            for s in result.scalars().all()
        ]

    async def get_history(self, fir_id: int) -> List[dict]:
        stmt = select(FIRAnalysisHistoryRecord).where(FIRAnalysisHistoryRecord.fir_id == fir_id).order_by(FIRAnalysisHistoryRecord.created_at.desc())
        result = await self.db.execute(stmt)
        return [
            {"id": h.id, "analysis_type": h.analysis_type, "model_used": h.model_used,
             "processing_time_ms": h.processing_time_ms,
             "created_at": str(h.created_at) if h.created_at else None}
            for h in result.scalars().all()
        ]

    async def get_stats(self) -> dict:
        total = (await self.db.execute(select(sql_func.count(FIRSuggestion.id)))).scalar() or 0
        analyses = (await self.db.execute(select(sql_func.count(FIRAnalysisHistoryRecord.id)))).scalar() or 0
        return {"total_suggestions": total, "total_analyses": analyses}

    async def _load_fir(self, fir_id: int) -> Optional[dict]:
        stmt = select(FIR).where(FIR.id == fir_id)
        result = await self.db.execute(stmt)
        fir = result.scalar()
        return {"id": fir.id, "title": fir.title, "description": fir.description,
                "crime_type": fir.crime_type, "district": fir.district} if fir else None

    async def _find_similar_crimes(self, fir: dict) -> List[dict]:
        stmt = select(Crime).where(Crime.crime_type_id.isnot(None)).limit(20)
        result = await self.db.execute(stmt)
        crimes = result.scalars().all()

        similar = []
        fir_text = f"{fir.get('title', '')} {fir.get('description', '')}".lower()
        for c in crimes:
            c_text = f"{c.title or ''} {c.description or ''}".lower()
            words1 = set(fir_text.split())
            words2 = set(c_text.split())
            overlap = len(words1 & words2) / max(len(words1 | words2), 1) * 100
            if overlap > 20:
                similar.append({"id": c.id, "title": c.title, "score": round(overlap, 1)})
        similar.sort(key=lambda x: x["score"], reverse=True)
        return similar[:5]

    def _find_mo_matches(self, text: str) -> List[str]:
        matches = []
        for category, keywords in MO_KEYWORDS.items():
            found = [kw for kw in keywords if kw in text]
            if found:
                matches.append(f"{category}: {', '.join(found)}")
        return matches

    async def _find_suspect_links(self, text: str) -> List[dict]:
        stmt = select(Suspect).limit(10)
        result = await self.db.execute(stmt)
        suspects = result.scalars().all()
        linked = []
        for s in suspects:
            desc = (s.description or "").lower()
            name = (s.name or "").lower()
            if any(w in text for w in name.split() if len(w) > 3):
                linked.append({"id": s.id, "name": s.name, "description": s.description or ""})
        return linked[:3]
