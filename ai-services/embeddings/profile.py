from typing import List, Dict
from embeddings.base import DomainEmbedder
import numpy as np
import structlog

logger = structlog.get_logger()


class ProfileEmbeddings:
    def __init__(self):
        self.embedder = DomainEmbedder("profile")

    def embed_profile(self, profile: Dict) -> list:
        text = self._prepare_text(profile)
        vec = self.embedder.embed_single(text)
        return vec.tolist()

    def embed_batch(self, profiles: List[Dict]) -> list:
        texts = [self._prepare_text(p) for p in profiles]
        if not self.embedder.is_fitted():
            self.embedder.fit(texts)
        vecs = self.embedder.embed(texts)
        return vecs.tolist()

    def _prepare_text(self, profile: Dict) -> str:
        parts = [
            str(profile.get("name", "")),
            str(profile.get("alias", "")),
            str(profile.get("description", "")),
            str(profile.get("mo_description", "")),
            str(profile.get("behavioral_profile", "")),
            str(profile.get("district", "")),
        ]
        return " ".join(p for p in parts if p)

    def similarity(self, p1: Dict, p2: Dict) -> float:
        v1 = np.array(self.embed_profile(p1))
        v2 = np.array(self.embed_profile(p2))
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-10))

    def find_similar_profiles(self, target: Dict, profiles: List[Dict], top_k: int = 5) -> List[Dict]:
        target_vec = np.array(self.embed_profile(target))
        results = []
        for p in profiles:
            p_vec = np.array(self.embed_profile(p))
            score = float(np.dot(target_vec, p_vec) / (np.linalg.norm(target_vec) * np.linalg.norm(p_vec) + 1e-10))
            results.append({**p, "similarity": round(score, 4)})
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
