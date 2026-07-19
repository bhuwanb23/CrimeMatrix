import json
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.crime import Crime
from app.models.crimetype import CrimeType
from app.models.district import District
from app.models.crime_pattern import CrimePattern
from app.models.pattern_occurrence import PatternOccurrence
from app.models.pattern_cluster import PatternCluster
import structlog
from datetime import datetime, timedelta
from collections import defaultdict

logger = structlog.get_logger()

MO_KEYWORDS = {
    "entry": ["break", "window", "door", "lock", "force", "pry", "drill"],
    "time": ["night", "morning", "evening", "dawn", "dusk", "late", "early"],
    "weapon": ["knife", "gun", "weapon", "threat", "force", "violence"],
    "target": ["jewelry", "cash", "electronics", "vehicle", "phone", "wallet"],
    "method": ["snatch", "grab", "con", "trick", "ambush", "distraction"],
    "transport": ["bike", "car", "walk", "bus", "auto", "escape"],
}


class PatternService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def detect_patterns(self) -> dict:
        stmt = select(Crime)
        result = await self.db.execute(stmt)
        crimes = result.scalars().all()

        if not crimes:
            return {"patterns_found": 0, "message": "No crimes to analyze"}

        crime_dicts = []
        for c in crimes:
            crime_dicts.append({
                "id": c.id,
                "title": c.title or "",
                "description": c.description or "",
                "crime_type_id": c.crime_type_id,
                "district_id": c.district_id,
                "status": c.status,
                "occurred_at": c.occurred_at,
                "created_at": c.created_at,
            })

        time_patterns = self._detect_time_patterns(crime_dicts)
        mo_patterns = self._detect_mo_patterns(crime_dicts)
        location_patterns = self._detect_location_patterns(crime_dicts)

        all_patterns = time_patterns + mo_patterns + location_patterns

        saved_count = 0
        for p in all_patterns:
            existing = await self._pattern_exists(p["name"])
            if not existing:
                await self._save_pattern(p)
                saved_count += 1

        return {
            "patterns_found": len(all_patterns),
            "patterns_saved": saved_count,
            "time_patterns": len(time_patterns),
            "mo_patterns": len(mo_patterns),
            "location_patterns": len(location_patterns),
        }

    async def get_patterns(self, pattern_type: str = None, crime_type: str = None) -> List[dict]:
        stmt = select(CrimePattern).where(CrimePattern.status == "active")
        if pattern_type:
            stmt = stmt.where(CrimePattern.pattern_type == pattern_type)
        if crime_type:
            stmt = stmt.where(CrimePattern.crime_type == crime_type)
        stmt = stmt.order_by(CrimePattern.confidence.desc())
        result = await self.db.execute(stmt)
        patterns = result.scalars().all()
        return [self._pattern_to_dict(p) for p in patterns]

    async def get_pattern(self, pattern_id: int) -> Optional[dict]:
        stmt = select(CrimePattern).where(CrimePattern.id == pattern_id)
        result = await self.db.execute(stmt)
        pattern = result.scalar()
        if not pattern:
            return None
        occurrences = await self._get_occurrences(pattern_id)
        return {**self._pattern_to_dict(pattern), "occurrences": occurrences}

    async def get_pattern_occurrences(self, pattern_id: int) -> List[dict]:
        return await self._get_occurrences(pattern_id)

    async def get_clusters(self) -> List[dict]:
        stmt = select(PatternCluster).order_by(PatternCluster.strength.desc())
        result = await self.db.execute(stmt)
        clusters = result.scalars().all()
        return [self._cluster_to_dict(c) for c in clusters]

    async def compare_patterns(self, p1_id: int, p2_id: int) -> dict:
        p1 = await self._load_pattern(p1_id)
        p2 = await self._load_pattern(p2_id)
        if not p1 or not p2:
            return {"error": "Pattern not found"}

        shared_chars = []
        if p1.get("crime_type") == p2.get("crime_type"):
            shared_chars.append(f"Same crime type: {p1['crime_type']}")
        if p1.get("time_pattern") == p2.get("time_pattern") and p1.get("time_pattern"):
            shared_chars.append(f"Same time pattern: {p1['time_pattern']}")
        if p1.get("location_pattern") == p2.get("location_pattern") and p1.get("location_pattern"):
            shared_chars.append(f"Same location pattern: {p1['location_pattern']}")

        mo1_words = set((p1.get("mo_summary") or "").lower().split())
        mo2_words = set((p2.get("mo_summary") or "").lower().split())
        mo_overlap = len(mo1_words & mo2_words) / max(len(mo1_words | mo2_words), 1) * 100

        overlap_score = (len(shared_chars) / 3 * 50) + (mo_overlap * 0.5)

        return {
            "pattern_1": p1,
            "pattern_2": p2,
            "shared_characteristics": shared_chars,
            "mo_overlap": round(mo_overlap, 1),
            "overlap_score": round(overlap_score, 1),
        }

    async def get_stats(self) -> dict:
        total = (await self.db.execute(select(sql_func.count(CrimePattern.id)))).scalar() or 0
        active = (await self.db.execute(
            select(sql_func.count(CrimePattern.id)).where(CrimePattern.status == "active")
        )).scalar() or 0
        occurrences = (await self.db.execute(select(sql_func.count(PatternOccurrence.id)))).scalar() or 0
        clusters = (await self.db.execute(select(sql_func.count(PatternCluster.id)))).scalar() or 0
        return {"total_patterns": total, "active_patterns": active, "total_occurrences": occurrences, "total_clusters": clusters}

    def _detect_time_patterns(self, crimes: List[dict]) -> List[dict]:
        hour_groups = defaultdict(list)
        for c in crimes:
            dt = c.get("occurred_at") or c.get("created_at")
            if dt:
                if isinstance(dt, str):
                    try:
                        dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
                    except Exception:
                        continue
                hour = dt.hour
                if 0 <= hour < 4:
                    hour_groups["night_0_4"].append(c)
                elif 4 <= hour < 8:
                    hour_groups["early_morning_4_8"].append(c)
                elif 8 <= hour < 12:
                    hour_groups["morning_8_12"].append(c)
                elif 12 <= hour < 16:
                    hour_groups["afternoon_12_16"].append(c)
                elif 16 <= hour < 20:
                    hour_groups["evening_16_20"].append(c)
                else:
                    hour_groups["late_night_20_24"].append(c)

        patterns = []
        time_labels = {
            "night_0_4": "Night (12 AM - 4 AM)",
            "early_morning_4_8": "Early Morning (4 AM - 8 AM)",
            "morning_8_12": "Morning (8 AM - 12 PM)",
            "afternoon_12_16": "Afternoon (12 PM - 4 PM)",
            "evening_16_20": "Evening (4 PM - 8 PM)",
            "late_night_20_24": "Late Night (8 PM - 12 AM)",
        }

        for period, period_crimes in hour_groups.items():
            if len(period_crimes) >= 3:
                crime_types = defaultdict(int)
                for c in period_crimes:
                    crime_types[c.get("crime_type_id")] = crime_types.get(c.get("crime_type_id"), 0) + 1
                dominant_type = max(crime_types, key=crime_types.get) if crime_types else None

                confidence = min(100, len(period_crimes) * 10)
                patterns.append({
                    "name": f"{time_labels.get(period, period)} Crime Cluster",
                    "description": f"{len(period_crimes)} crimes detected during {time_labels.get(period, period).lower()}",
                    "pattern_type": "time",
                    "time_pattern": period,
                    "confidence": confidence,
                    "frequency": len(period_crimes),
                    "crime_ids": [c["id"] for c in period_crimes],
                })

        return patterns

    def _detect_mo_patterns(self, crimes: List[dict]) -> List[dict]:
        desc_groups = defaultdict(list)
        for c in crimes:
            desc = (c.get("description") or "").lower()
            if not desc:
                continue
            categories = set()
            for cat, keywords in MO_KEYWORDS.items():
                if any(kw in desc for kw in keywords):
                    categories.add(cat)
            if categories:
                key = frozenset(categories)
                desc_groups[key].append(c)

        patterns = []
        for categories, group_crimes in desc_groups.items():
            if len(group_crimes) >= 3:
                cat_names = sorted(categories)
                confidence = min(100, len(group_crimes) * 12)
                patterns.append({
                    "name": f"MO Pattern: {', '.join(cat_names[:3])}",
                    "description": f"{len(group_crimes)} crimes share MO characteristics: {', '.join(cat_names)}",
                    "pattern_type": "mo",
                    "mo_summary": ", ".join(cat_names),
                    "confidence": confidence,
                    "frequency": len(group_crimes),
                    "crime_ids": [c["id"] for c in group_crimes],
                })

        return patterns

    def _detect_location_patterns(self, crimes: List[dict]) -> List[dict]:
        district_groups = defaultdict(list)
        for c in crimes:
            did = c.get("district_id")
            if did:
                district_groups[did].append(c)

        patterns = []
        for district_id, group_crimes in district_groups.items():
            if len(group_crimes) >= 3:
                crime_types = defaultdict(int)
                for c in group_crimes:
                    crime_types[c.get("crime_type_id")] += 1
                dominant = max(crime_types, key=crime_types.get) if crime_types else None
                confidence = min(100, len(group_crimes) * 8)
                patterns.append({
                    "name": f"District Cluster: District #{district_id}",
                    "description": f"{len(group_crimes)} crimes concentrated in district #{district_id}",
                    "pattern_type": "location",
                    "location_pattern": f"district_{district_id}",
                    "confidence": confidence,
                    "frequency": len(group_crimes),
                    "crime_ids": [c["id"] for c in group_crimes],
                })

        return patterns

    async def _pattern_exists(self, name: str) -> bool:
        stmt = select(CrimePattern).where(CrimePattern.name == name)
        result = await self.db.execute(stmt)
        return result.scalar() is not None

    async def _save_pattern(self, pattern_data: dict):
        crime_ids = pattern_data.pop("crime_ids", [])
        pattern = CrimePattern(
            name=pattern_data["name"],
            description=pattern_data.get("description"),
            pattern_type=pattern_data["pattern_type"],
            crime_type=pattern_data.get("crime_type"),
            confidence=pattern_data.get("confidence", 0),
            frequency=pattern_data.get("frequency", 0),
            time_pattern=pattern_data.get("time_pattern"),
            location_pattern=pattern_data.get("location_pattern"),
            mo_summary=pattern_data.get("mo_summary"),
        )
        self.db.add(pattern)
        await self.db.flush()

        for crime_id in crime_ids[:20]:
            occ = PatternOccurrence(pattern_id=pattern.id, crime_id=crime_id, similarity_score=pattern_data.get("confidence", 0))
            self.db.add(occ)

        await self.db.commit()

    async def _get_occurrences(self, pattern_id: int) -> List[dict]:
        stmt = select(PatternOccurrence).where(PatternOccurrence.pattern_id == pattern_id)
        result = await self.db.execute(stmt)
        occs = result.scalars().all()
        return [{"id": o.id, "crime_id": o.crime_id, "similarity_score": o.similarity_score} for o in occs]

    async def _load_pattern(self, pattern_id: int) -> Optional[dict]:
        stmt = select(CrimePattern).where(CrimePattern.id == pattern_id)
        result = await self.db.execute(stmt)
        p = result.scalar()
        return self._pattern_to_dict(p) if p else None

    def _pattern_to_dict(self, p: CrimePattern) -> dict:
        return {
            "id": p.id, "name": p.name, "description": p.description,
            "pattern_type": p.pattern_type, "crime_type": p.crime_type,
            "confidence": p.confidence, "frequency": p.frequency,
            "time_pattern": p.time_pattern, "location_pattern": p.location_pattern,
            "mo_summary": p.mo_summary, "status": p.status,
            "first_seen": str(p.first_seen) if p.first_seen else None,
            "last_seen": str(p.last_seen) if p.last_seen else None,
            "created_at": str(p.created_at) if p.created_at else None,
        }

    def _cluster_to_dict(self, c: PatternCluster) -> dict:
        return {
            "id": c.id, "name": c.name, "description": c.description,
            "pattern_ids": json.loads(c.pattern_ids) if c.pattern_ids else [],
            "cluster_type": c.cluster_type, "strength": c.strength,
        }
