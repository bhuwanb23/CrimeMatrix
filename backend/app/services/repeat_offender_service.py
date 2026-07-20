import json
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.criminal import Criminal
from app.models.suspect import Suspect
from app.models.crime import Crime
from app.models.repeat_offender import RepeatOffender
from app.models.offender_score import OffenderScore
import structlog
from datetime import datetime, timedelta
from collections import defaultdict

logger = structlog.get_logger()


class RepeatOffenderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze_offenders(self) -> dict:
        # Get all suspects with crimes
        stmt = select(Suspect)
        result = await self.db.execute(stmt)
        suspects = result.scalars().all()

        analyzed = 0
        for suspect in suspects:
            # Count crimes related to this suspect (by name match in crime descriptions)
            crime_count = await self._count_crimes_for_name(suspect.name or "")
            if crime_count < 2:
                continue

            # Calculate scores
            frequency = min(100, crime_count * 15)
            recency = await self._calculate_recency(suspect.name or "")
            severity = await self._calculate_severity(suspect.name or "")
            geographic = await self._calculate_geographic(suspect.name or "")

            overall = (frequency * 0.35 + recency * 0.25 + severity * 0.25 + geographic * 0.15)
            risk_level = "critical" if overall > 80 else "high" if overall > 60 else "medium" if overall > 40 else "low"

            risk_factors = []
            if frequency > 60: risk_factors.append(f"High frequency: {crime_count} offenses")
            if recency > 70: risk_factors.append("Recent offense activity")
            if severity > 60: risk_factors.append("Involves serious crime types")
            if geographic > 50: risk_factors.append("Active across multiple districts")

            # Save or update
            existing = await self._offender_exists(suspect.id)
            if existing:
                existing.total_offenses = crime_count
                existing.frequency_score = frequency
                existing.recency_score = recency
                existing.severity_score = severity
                existing.geographic_score = geographic
                existing.overall_score = round(overall, 1)
                existing.risk_level = risk_level
                existing.risk_factors = json.dumps(risk_factors)
            else:
                offender = RepeatOffender(
                    suspect_id=suspect.id,
                    offender_name=suspect.name,
                    total_offenses=crime_count,
                    frequency_score=frequency,
                    recency_score=recency,
                    severity_score=severity,
                    geographic_score=geographic,
                    overall_score=round(overall, 1),
                    risk_level=risk_level,
                    risk_factors=json.dumps(risk_factors),
                )
                self.db.add(offender)
            analyzed += 1

        await self.db.commit()
        return {"offenders_identified": analyzed, "total_suspects": len(suspects)}

    async def get_offenders(self, risk_level: str = None) -> List[dict]:
        stmt = select(RepeatOffender).where(RepeatOffender.status == "active")
        if risk_level:
            stmt = stmt.where(RepeatOffender.risk_level == risk_level)
        stmt = stmt.order_by(RepeatOffender.overall_score.desc())
        result = await self.db.execute(stmt)
        return [self._offender_to_dict(o) for o in result.scalars().all()]

    async def get_offender(self, offender_id: int) -> Optional[dict]:
        stmt = select(RepeatOffender).where(RepeatOffender.id == offender_id)
        result = await self.db.execute(stmt)
        o = result.scalar()
        if not o:
            return None
        scores = await self._get_scores(offender_id)
        return {**self._offender_to_dict(o), "scores": scores}

    async def get_rankings(self, limit: int = 10) -> List[dict]:
        stmt = (
            select(RepeatOffender)
            .where(RepeatOffender.status == "active")
            .order_by(RepeatOffender.overall_score.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return [self._offender_to_dict(o) for o in result.scalars().all()]

    async def get_stats(self) -> dict:
        total = (await self.db.execute(select(sql_func.count(RepeatOffender.id)))).scalar() or 0
        critical = (await self.db.execute(
            select(sql_func.count(RepeatOffender.id)).where(RepeatOffender.risk_level == "critical")
        )).scalar() or 0
        high = (await self.db.execute(
            select(sql_func.count(RepeatOffender.id)).where(RepeatOffender.risk_level == "high")
        )).scalar() or 0
        return {"total_offenders": total, "critical": critical, "high": high}

    async def _count_crimes_for_name(self, name: str) -> int:
        if not name:
            return 0
        stmt = select(sql_func.count(Crime.id)).where(Crime.title.ilike(f"%{name}%"))
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def _calculate_recency(self, name: str) -> float:
        stmt = select(Crime.created_at).where(Crime.title.ilike(f"%{name}%")).order_by(Crime.created_at.desc()).limit(1)
        result = await self.db.execute(stmt)
        latest = result.scalar()
        if not latest:
            return 0
        if isinstance(latest, str):
            try:
                latest = datetime.fromisoformat(latest.replace("Z", "+00:00"))
            except Exception:
                return 0
        days_ago = (datetime.utcnow() - latest).days
        if days_ago <= 7: return 100
        if days_ago <= 30: return 80
        if days_ago <= 90: return 60
        if days_ago <= 365: return 40
        return 20

    async def _calculate_severity(self, name: str) -> float:
        stmt = select(Crime).where(Crime.title.ilike(f"%{name}%"))
        result = await self.db.execute(stmt)
        crimes = result.scalars().all()
        if not crimes:
            return 0
        severity_map = {"murder": 100, "robbery": 80, "assault": 70, "theft": 50, "fraud": 40}
        max_sev = 0
        for c in crimes:
            title = (c.title or "").lower()
            for keyword, sev in severity_map.items():
                if keyword in title:
                    max_sev = max(max_sev, sev)
        return max_sev if max_sev > 0 else 30

    async def _calculate_geographic(self, name: str) -> float:
        stmt = select(Crime).where(Crime.title.ilike(f"%{name}%"))
        result = await self.db.execute(stmt)
        crimes = result.scalars().all()
        districts = set()
        for c in crimes:
            if c.district_id:
                districts.add(c.district_id)
        if len(districts) >= 3: return 100
        if len(districts) == 2: return 60
        return 30 if len(districts) == 1 else 0

    async def _offender_exists(self, suspect_id: int) -> Optional[RepeatOffender]:
        stmt = select(RepeatOffender).where(RepeatOffender.suspect_id == suspect_id)
        result = await self.db.execute(stmt)
        return result.scalar()

    async def _get_scores(self, offender_id: int) -> List[dict]:
        stmt = select(OffenderScore).where(OffenderScore.offender_id == offender_id)
        result = await self.db.execute(stmt)
        return [
            {"dimension": s.dimension, "score": s.score, "details": s.details}
            for s in result.scalars().all()
        ]

    def _offender_to_dict(self, o: RepeatOffender) -> dict:
        return {
            "id": o.id, "criminal_id": o.criminal_id, "suspect_id": o.suspect_id,
            "offender_name": o.offender_name, "total_offenses": o.total_offenses,
            "frequency_score": o.frequency_score, "recency_score": o.recency_score,
            "severity_score": o.severity_score, "geographic_score": o.geographic_score,
            "overall_score": o.overall_score, "risk_level": o.risk_level,
            "risk_factors": json.loads(o.risk_factors) if o.risk_factors else [],
            "status": o.status,
        }
