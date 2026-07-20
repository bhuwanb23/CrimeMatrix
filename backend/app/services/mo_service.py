import json
import re
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.crime import Crime
from app.models.mo_profile import MOProfile
from app.models.mo_embedding import MOEmbedding
from app.models.mo_similarity_record import MOSimilarityRecord
import structlog
from datetime import datetime

logger = structlog.get_logger()

MO_KEYWORDS = {
    "entry": ["break", "window", "door", "lock", "force", "pry", "drill", "climb", "jump"],
    "exit": ["run", "flee", "escape", "drive", "walk", "bike", "auto"],
    "time": ["night", "morning", "evening", "dawn", "dusk", "late", "early", "noon", "midnight"],
    "weapon": ["knife", "gun", "weapon", "threat", "force", "violence", "blade", "firearm"],
    "target": ["jewelry", "cash", "electronics", "vehicle", "phone", "wallet", "gold", "laptop"],
    "method": ["snatch", "grab", "con", "trick", "ambush", "distraction", "fraud", "deception"],
    "transport": ["bike", "car", "walk", "bus", "auto", "escape", "motorcycle"],
    "location": ["house", "shop", "street", "market", "station", "road", "alley", "residence"],
}


class MOService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_fingerprint(self, crime_id: int) -> dict:
        stmt = select(Crime).where(Crime.id == crime_id)
        result = await self.db.execute(stmt)
        crime = result.scalar()
        if not crime:
            return {"error": "Crime not found"}

        text = f"{crime.title or ''} {crime.description or ''}".lower()

        features = self._extract_features(text)
        mo_text = self._build_mo_text(features)

        # Calculate confidence
        non_empty = sum(1 for v in features.values() if v)
        confidence = min(100, non_empty * 12.5)

        # Save profile
        existing = await self._profile_exists(crime_id)
        if existing:
            for k, v in features.items():
                setattr(existing, k, v)
            existing.mo_text = mo_text
            existing.fingerprint_json = json.dumps(features)
            existing.confidence = confidence
            profile_id = existing.id
        else:
            profile = MOProfile(
                crime_id=crime_id,
                entry_method=features.get("entry_method", ""),
                exit_method=features.get("exit_method", ""),
                timing_pattern=features.get("timing_pattern", ""),
                weapon_type=features.get("weapon_type", ""),
                target_type=features.get("target_type", ""),
                location_pattern=features.get("location_pattern", ""),
                victim_profile=features.get("victim_profile", ""),
                escape_method=features.get("escape_method", ""),
                mo_text=mo_text,
                fingerprint_json=json.dumps(features),
                confidence=confidence,
            )
            self.db.add(profile)
            await self.db.flush()
            profile_id = profile.id

        # Save embedding
        embedding = self._create_embedding(features)
        existing_emb = await self._embedding_exists(profile_id)
        if existing_emb:
            existing_emb.vector_json = json.dumps(embedding)
            existing_emb.content = mo_text
        else:
            emb = MOEmbedding(profile_id=profile_id, dimension="combined", vector_json=json.dumps(embedding), content=mo_text)
            self.db.add(emb)

        await self.db.commit()

        return {
            "profile_id": profile_id,
            "crime_id": crime_id,
            "features": features,
            "confidence": confidence,
            "mo_text": mo_text,
        }

    async def get_profiles(self, crime_id: int = None) -> List[dict]:
        stmt = select(MOProfile)
        if crime_id:
            stmt = stmt.where(MOProfile.crime_id == crime_id)
        stmt = stmt.order_by(MOProfile.confidence.desc())
        result = await self.db.execute(stmt)
        return [self._profile_to_dict(p) for p in result.scalars().all()]

    async def get_profile(self, profile_id: int) -> Optional[dict]:
        stmt = select(MOProfile).where(MOProfile.id == profile_id)
        result = await self.db.execute(stmt)
        p = result.scalar()
        return self._profile_to_dict(p) if p else None

    async def compare_profiles(self, profile_id_1: int, profile_id_2: int) -> dict:
        p1 = await self._load_profile(profile_id_1)
        p2 = await self._load_profile(profile_id_2)
        if not p1 or not p2:
            return {"error": "Profile not found"}

        # Calculate similarity
        features1 = json.loads(p1.get("fingerprint_json", "{}"))
        features2 = json.loads(p2.get("fingerprint_json", "{}"))

        shared = []
        total = 0
        matched = 0
        for key in MO_KEYWORDS.keys():
            v1 = features1.get(key, "")
            v2 = features2.get(key, "")
            total += 1
            if v1 and v2 and v1 == v2:
                matched += 1
                shared.append(key)
            elif v1 and v2:
                # Partial match - check keyword overlap
                words1 = set(v1.lower().split())
                words2 = set(v2.lower().split())
                overlap = words1 & words2
                if overlap:
                    matched += 0.5
                    shared.append(f"{key} (partial)")

        score = round((matched / max(total, 1)) * 100, 1)
        match_level = "strong" if score > 70 else "moderate" if score > 40 else "weak"

        # Save comparison
        existing = await self._similarity_exists(profile_id_1, profile_id_2)
        if existing:
            existing.similarity_score = score
            existing.match_level = match_level
            existing.shared_features = json.dumps(shared)
        else:
            sim = MOSimilarityRecord(
                profile_id_1=min(profile_id_1, profile_id_2),
                profile_id_2=max(profile_id_1, profile_id_2),
                similarity_score=score,
                match_level=match_level,
                shared_features=json.dumps(shared),
            )
            self.db.add(sim)

        await self.db.commit()

        return {
            "profile_1": p1,
            "profile_2": p2,
            "similarity_score": score,
            "match_level": match_level,
            "shared_features": shared,
        }

    async def find_similar(self, profile_id: int, top_k: int = 5) -> List[dict]:
        profile = await self._load_profile(profile_id)
        if not profile:
            return []

        stmt = select(MOProfile).where(MOProfile.id != profile_id)
        result = await self.db.execute(stmt)
        all_profiles = result.scalars().all()

        scored = []
        for p in all_profiles:
            p_features = json.loads(p.fingerprint_json or "{}")
            target_features = json.loads(profile.get("fingerprint_json", "{}"))

            matches = 0
            for key in MO_KEYWORDS.keys():
                v1 = target_features.get(key, "")
                v2 = p_features.get(key, "")
                if v1 and v2 and v1 == v2:
                    matches += 1
                elif v1 and v2:
                    words1 = set(v1.lower().split())
                    words2 = set(v2.lower().split())
                    if words1 & words2:
                        matches += 0.5

            score = round((matches / max(len(MO_KEYWORDS), 1)) * 100, 1)
            if score > 0:
                scored.append({
                    "profile_id": p.id,
                    "crime_id": p.crime_id,
                    "similarity_score": score,
                    "match_level": "strong" if score > 70 else "moderate" if score > 40 else "weak",
                })

        scored.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored[:top_k]

    async def batch_fingerprint(self) -> dict:
        stmt = select(Crime)
        result = await self.db.execute(stmt)
        crimes = result.scalars().all()

        created = 0
        for crime in crimes:
            existing = await self._profile_exists(crime.id)
            if not existing:
                await self.create_fingerprint(crime.id)
                created += 1

        return {"crimes_processed": len(crimes), "new_profiles": created}

    async def get_stats(self) -> dict:
        total = (await self.db.execute(select(sql_func.count(MOProfile.id)))).scalar() or 0
        comparisons = (await self.db.execute(select(sql_func.count(MOSimilarityRecord.id)))).scalar() or 0
        avg_score = (await self.db.execute(select(sql_func.avg(MOSimilarityRecord.similarity_score)))).scalar()
        return {"total_profiles": total, "total_comparisons": comparisons, "avg_similarity": round(avg_score or 0, 1)}

    def _extract_features(self, text: str) -> dict:
        features = {}
        for category, keywords in MO_KEYWORDS.items():
            found = [kw for kw in keywords if kw in text]
            features[category] = ", ".join(found) if found else ""
        return features

    def _build_mo_text(self, features: dict) -> str:
        parts = []
        for cat, val in features.items():
            if val:
                parts.append(f"{cat}: {val}")
        return "; ".join(parts) if parts else "No MO features detected"

    def _create_embedding(self, features: dict) -> list:
        # Simple TF-IDF-like embedding based on keyword presence
        all_keywords = []
        for keywords in MO_KEYWORDS.values():
            all_keywords.extend(keywords)

        embedding = []
        text = " ".join(features.values()).lower()
        for kw in all_keywords:
            embedding.append(1.0 if kw in text else 0.0)
        return embedding

    async def _profile_exists(self, crime_id: int) -> Optional[MOProfile]:
        stmt = select(MOProfile).where(MOProfile.crime_id == crime_id)
        result = await self.db.execute(stmt)
        return result.scalar()

    async def _embedding_exists(self, profile_id: int) -> Optional[MOEmbedding]:
        stmt = select(MOEmbedding).where(MOEmbedding.profile_id == profile_id)
        result = await self.db.execute(stmt)
        return result.scalar()

    async def _similarity_exists(self, p1: int, p2: int) -> Optional[MOSimilarityRecord]:
        stmt = select(MOSimilarityRecord).where(
            MOSimilarityRecord.profile_id_1 == min(p1, p2),
            MOSimilarityRecord.profile_id_2 == max(p1, p2),
        )
        result = await self.db.execute(stmt)
        return result.scalar()

    async def _load_profile(self, profile_id: int) -> Optional[dict]:
        stmt = select(MOProfile).where(MOProfile.id == profile_id)
        result = await self.db.execute(stmt)
        p = result.scalar()
        return self._profile_to_dict(p) if p else None

    def _profile_to_dict(self, p: MOProfile) -> dict:
        return {
            "id": p.id, "crime_id": p.crime_id, "case_id": p.case_id,
            "entry_method": p.entry_method, "exit_method": p.exit_method,
            "timing_pattern": p.timing_pattern, "weapon_type": p.weapon_type,
            "target_type": p.target_type, "location_pattern": p.location_pattern,
            "victim_profile": p.victim_profile, "escape_method": p.escape_method,
            "mo_text": p.mo_text, "confidence": p.confidence,
            "fingerprint": json.loads(p.fingerprint_json) if p.fingerprint_json else {},
        }
