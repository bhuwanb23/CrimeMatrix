import json
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.criminal import Criminal
from app.models.suspect import Suspect
from app.models.crime import Crime
from app.models.evidence import Evidence
from app.models.behavior_profile import BehaviorProfile
from app.models.behavior_feature import BehaviorFeature
from app.models.case_status_log import CaseStatusLog
import structlog
from datetime import datetime
from collections import defaultdict

logger = structlog.get_logger()

TIMING_KEYWORDS = {"night": "night", "morning": "morning", "evening": "evening", "dawn": "dawn", "dusk": "dusk", "late": "late_night", "early": "early_morning"}
WEAPON_KEYWORDS = {"knife": "blade", "gun": "firearm", "weapon": "armed", "threat": "threat", "force": "force", "violence": "violence"}
TARGET_KEYWORDS = {"jewelry": "jewelry", "cash": "cash", "electronics": "electronics", "vehicle": "vehicle", "phone": "phone", "wallet": "wallet"}
METHOD_KEYWORDS = {"snatch": "snatch", "grab": "grab", "con": "con", "trick": "trick", "ambush": "ambush", "distraction": "distraction"}
ENTRY_KEYWORDS = {"break": "break_in", "window": "window_entry", "door": "door_entry", "lock": "lock_picking", "force": "forced_entry", "pry": "pry_tool"}


class BehaviorService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze_criminal(self, criminal_id: int) -> dict:
        stmt = select(Criminal).where(Criminal.id == criminal_id)
        result = await self.db.execute(stmt)
        criminal = result.scalar()
        if not criminal:
            return {"error": "Criminal not found"}

        mo = criminal.mo_description or ""
        profile = criminal.behavioral_profile or ""

        # Analyze timing patterns
        timing = self._analyze_timing(mo, profile)
        # Analyze weapon patterns
        weapon = self._analyze_weapon(mo, profile)
        # Analyze target patterns
        target = self._analyze_target(mo, profile)
        # Analyze method patterns
        method = self._analyze_method(mo, profile)
        # Analyze entry patterns
        entry = self._analyze_entry(mo, profile)

        # Calculate risk score
        risk_score = self._calculate_risk_score(timing, weapon, target, method, entry, criminal.risk_score or 0)
        risk_level = "critical" if risk_score > 80 else "high" if risk_score > 60 else "medium" if risk_score > 40 else "low"

        # Save profiles
        profiles = [
            {"profile_type": "timing", "pattern_description": timing["description"], "confidence": timing["confidence"], "features": timing["features"]},
            {"profile_type": "weapon", "pattern_description": weapon["description"], "confidence": weapon["confidence"], "features": weapon["features"]},
            {"profile_type": "target", "pattern_description": target["description"], "confidence": target["confidence"], "features": target["features"]},
            {"profile_type": "method", "pattern_description": method["description"], "confidence": method["confidence"], "features": method["features"]},
            {"profile_type": "entry", "pattern_description": entry["description"], "confidence": entry["confidence"], "features": entry["features"]},
        ]

        saved_ids = []
        for p in profiles:
            existing = await self._profile_exists(criminal_id, p["profile_type"])
            if existing:
                existing.pattern_description = p["pattern_description"]
                existing.confidence = p["confidence"]
                existing.features_json = json.dumps(p["features"])
                existing.risk_score = risk_score
                existing.risk_level = risk_level
                existing.last_analyzed = datetime.utcnow()
                saved_ids.append(existing.id)
            else:
                bp = BehaviorProfile(
                    criminal_id=criminal_id,
                    profile_type=p["profile_type"],
                    pattern_description=p["pattern_description"],
                    confidence=p["confidence"],
                    features_json=json.dumps(p["features"]),
                    risk_score=risk_score,
                    risk_level=risk_level,
                    last_analyzed=datetime.utcnow(),
                )
                self.db.add(bp)
                await self.db.flush()
                saved_ids.append(bp.id)

                for fname, fval in p["features"].items():
                    bf = BehaviorFeature(profile_id=bp.id, feature_name=fname, feature_value=str(fval), weight=fval.get("weight", 0) if isinstance(fval, dict) else 1.0)
                    self.db.add(bf)

        await self.db.commit()

        return {
            "criminal_id": criminal_id,
            "alias": criminal.alias,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "profiles": {p["profile_type"]: p["pattern_description"] for p in profiles},
            "analyzed_at": datetime.utcnow().isoformat(),
        }

    async def get_profiles(self, criminal_id: int = None) -> List[dict]:
        stmt = select(BehaviorProfile)
        if criminal_id:
            stmt = stmt.where(BehaviorProfile.criminal_id == criminal_id)
        stmt = stmt.order_by(BehaviorProfile.risk_score.desc())
        result = await self.db.execute(stmt)
        profiles = result.scalars().all()
        return [self._profile_to_dict(p) for p in profiles]

    async def get_risk_assessment(self) -> List[dict]:
        stmt = select(BehaviorProfile).where(BehaviorProfile.profile_type == "timing").order_by(BehaviorProfile.risk_score.desc())
        result = await self.db.execute(stmt)
        profiles = result.scalars().all()

        assessments = []
        for p in profiles:
            criminal = await self._load_criminal(p.criminal_id)
            assessments.append({
                "criminal_id": p.criminal_id,
                "alias": criminal.get("alias", f"Criminal #{p.criminal_id}") if criminal else f"Criminal #{p.criminal_id}",
                "risk_score": p.risk_score,
                "risk_level": p.risk_level,
                "profiles_analyzed": await self._count_profiles(p.criminal_id),
                "last_analyzed": str(p.last_analyzed) if p.last_analyzed else None,
            })

        return assessments

    async def get_features(self, profile_id: int) -> List[dict]:
        stmt = select(BehaviorFeature).where(BehaviorFeature.profile_id == profile_id)
        result = await self.db.execute(stmt)
        return [
            {"id": f.id, "feature_name": f.feature_name, "feature_value": f.feature_value, "weight": f.weight}
            for f in result.scalars().all()
        ]

    async def get_stats(self) -> dict:
        total = (await self.db.execute(select(sql_func.count(BehaviorProfile.id)))).scalar() or 0
        criminals = (await self.db.execute(select(sql_func.count(sql_func.distinct(BehaviorProfile.criminal_id))))).scalar() or 0
        high_risk = (await self.db.execute(
            select(sql_func.count(BehaviorProfile.id)).where(BehaviorProfile.risk_level.in_(["high", "critical"]))
        )).scalar() or 0
        return {"total_profiles": total, "criminals_profiled": criminals, "high_risk": high_risk}

    def _analyze_timing(self, mo: str, profile: str) -> dict:
        text = f"{mo} {profile}".lower()
        features = {}
        for kw, label in TIMING_KEYWORDS.items():
            if kw in text:
                features[label] = {"present": True, "weight": 0.8}
        confidence = min(100, len(features) * 25)
        desc = f"Timing patterns: {', '.join(features.keys())}" if features else "No clear timing pattern detected"
        return {"description": desc, "confidence": confidence, "features": features}

    def _analyze_weapon(self, mo: str, profile: str) -> dict:
        text = f"{mo} {profile}".lower()
        features = {}
        for kw, label in WEAPON_KEYWORDS.items():
            if kw in text:
                features[label] = {"present": True, "weight": 0.9}
        confidence = min(100, len(features) * 25)
        desc = f"Weapon patterns: {', '.join(features.keys())}" if features else "No clear weapon pattern"
        return {"description": desc, "confidence": confidence, "features": features}

    def _analyze_target(self, mo: str, profile: str) -> dict:
        text = f"{mo} {profile}".lower()
        features = {}
        for kw, label in TARGET_KEYWORDS.items():
            if kw in text:
                features[label] = {"present": True, "weight": 0.8}
        confidence = min(100, len(features) * 20)
        desc = f"Target patterns: {', '.join(features.keys())}" if features else "No clear target pattern"
        return {"description": desc, "confidence": confidence, "features": features}

    def _analyze_method(self, mo: str, profile: str) -> dict:
        text = f"{mo} {profile}".lower()
        features = {}
        for kw, label in METHOD_KEYWORDS.items():
            if kw in text:
                features[label] = {"present": True, "weight": 0.7}
        confidence = min(100, len(features) * 25)
        desc = f"Method patterns: {', '.join(features.keys())}" if features else "No clear method pattern"
        return {"description": desc, "confidence": confidence, "features": features}

    def _analyze_entry(self, mo: str, profile: str) -> dict:
        text = f"{mo} {profile}".lower()
        features = {}
        for kw, label in ENTRY_KEYWORDS.items():
            if kw in text:
                features[label] = {"present": True, "weight": 0.8}
        confidence = min(100, len(features) * 20)
        desc = f"Entry patterns: {', '.join(features.keys())}" if features else "No clear entry pattern"
        return {"description": desc, "confidence": confidence, "features": features}

    def _calculate_risk_score(self, timing, weapon, target, method, entry, base_risk) -> float:
        scores = [timing["confidence"], weapon["confidence"], target["confidence"], method["confidence"], entry["confidence"]]
        avg = sum(scores) / max(len(scores), 1)
        weighted = avg * 0.6 + base_risk * 100 * 0.4
        return min(100, round(weighted, 1))

    async def _profile_exists(self, criminal_id: int, profile_type: str) -> Optional[BehaviorProfile]:
        stmt = select(BehaviorProfile).where(
            BehaviorProfile.criminal_id == criminal_id,
            BehaviorProfile.profile_type == profile_type,
        )
        result = await self.db.execute(stmt)
        return result.scalar()

    async def _count_profiles(self, criminal_id: int) -> int:
        return (await self.db.execute(
            select(sql_func.count(BehaviorProfile.id)).where(BehaviorProfile.criminal_id == criminal_id)
        )).scalar() or 0

    async def _load_criminal(self, criminal_id: int) -> Optional[dict]:
        stmt = select(Criminal).where(Criminal.id == criminal_id)
        result = await self.db.execute(stmt)
        c = result.scalar()
        return {"id": c.id, "alias": c.alias, "risk_score": c.risk_score} if c else None

    def _profile_to_dict(self, p: BehaviorProfile) -> dict:
        return {
            "id": p.id, "criminal_id": p.criminal_id, "profile_type": p.profile_type,
            "pattern_description": p.pattern_description, "confidence": p.confidence,
            "risk_level": p.risk_level, "risk_score": p.risk_score,
            "last_analyzed": str(p.last_analyzed) if p.last_analyzed else None,
        }
