from typing import Dict, List, Optional
from embeddings.base import DomainEmbedder
import numpy as np
import structlog

logger = structlog.get_logger()


class CaseEmbeddingGenerator:
    def __init__(self):
        self.mo_embedder = DomainEmbedder("mo_fingerprint")
        self.desc_embedder = DomainEmbedder("fir")
        self.evidence_embedder = DomainEmbedder("evidence")
        self.profile_embedder = DomainEmbedder("profile")

    def generate_embeddings(self, case_profile: dict) -> Dict[str, list]:
        dimensions = {}

        mo_text = self._prepare_mo_text(case_profile)
        if mo_text.strip():
            dimensions["mo"] = self._embed_text(mo_text, self.mo_embedder)

        loc_text = self._prepare_location_text(case_profile)
        if loc_text.strip():
            dimensions["location"] = self._embed_text(loc_text, self.desc_embedder)

        time_text = self._prepare_time_text(case_profile)
        if time_text.strip():
            dimensions["time"] = self._embed_text(time_text, self.desc_embedder)

        sus_text = self._prepare_suspects_text(case_profile)
        if sus_text.strip():
            dimensions["suspects"] = self._embed_text(sus_text, self.profile_embedder)

        ev_text = self._prepare_evidence_text(case_profile)
        if ev_text.strip():
            dimensions["evidence"] = self._embed_text(ev_text, self.evidence_embedder)

        veh_text = self._prepare_vehicles_text(case_profile)
        if veh_text.strip():
            dimensions["vehicles"] = self._embed_text(veh_text, self.desc_embedder)

        combined_text = " ".join([mo_text, loc_text, sus_text, ev_text, veh_text]).strip()
        if combined_text:
            dimensions["combined"] = self._embed_text(combined_text, self.desc_embedder)

        return dimensions

    def similarity(self, vec1: list, vec2: list) -> float:
        a, b = np.array(vec1), np.array(vec2)
        norm_a, norm_b = np.linalg.norm(a), np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    def find_similar(self, target_vec: list, candidates: List[Dict], top_k: int = 5) -> List[Dict]:
        results = []
        target = np.array(target_vec)
        target_norm = np.linalg.norm(target)
        if target_norm == 0:
            return []

        for c in candidates:
            c_vec = np.array(c.get("vector", []))
            c_norm = np.linalg.norm(c_vec)
            if c_norm == 0:
                continue
            score = float(np.dot(target, c_vec) / (target_norm * c_norm))
            results.append({**c, "similarity": round(score * 100, 1)})

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def _embed_text(self, text: str, embedder: DomainEmbedder) -> list:
        try:
            vec = embedder.embed_single(text)
            return vec.tolist()
        except Exception as e:
            logger.warning("embed_error", error=str(e))
            return []

    def _prepare_mo_text(self, profile: dict) -> str:
        parts = [
            str(profile.get("description", "")),
            str(profile.get("crime_type", "")),
            str(profile.get("title", "")),
        ]
        return " ".join(p for p in parts if p)

    def _prepare_location_text(self, profile: dict) -> str:
        parts = [
            str(profile.get("district", "")),
            str(profile.get("title", "")),
        ]
        return " ".join(p for p in parts if p)

    def _prepare_time_text(self, profile: dict) -> str:
        created = profile.get("created_at", "")
        if not created:
            return ""
        return f"crime occurred time case filing {created}"

    def _prepare_suspects_text(self, profile: dict) -> str:
        suspects = profile.get("suspects", [])
        if not suspects:
            return ""
        parts = []
        for s in suspects:
            name = s.get("name", "")
            district = s.get("district", "")
            desc = s.get("description", "") or s.get("physical_description", "")
            age = s.get("age", "")
            parts.append(f"{name} {district} {desc} {age}".strip())
        return " ".join(parts)

    def _prepare_evidence_text(self, profile: dict) -> str:
        evidence = profile.get("evidence", [])
        if not evidence:
            return ""
        parts = []
        for e in evidence:
            etype = e.get("evidence_type", "")
            desc = e.get("description", "")
            parts.append(f"{etype} {desc}".strip())
        return " ".join(parts)

    def _prepare_vehicles_text(self, profile: dict) -> str:
        vehicles = profile.get("vehicles", [])
        if not vehicles:
            return ""
        parts = []
        for v in vehicles:
            make = v.get("make", "")
            model = v.get("model", "")
            color = v.get("color", "")
            vtype = v.get("type", "")
            parts.append(f"{make} {model} {color} {vtype}".strip())
        return " ".join(parts)
