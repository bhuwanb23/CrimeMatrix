from typing import List, Dict
from embeddings.base import DomainEmbedder
import numpy as np
import structlog

logger = structlog.get_logger()


class MOFingerprintEmbeddings:
    def __init__(self):
        self.embedder = DomainEmbedder("mo_fingerprint")

    def embed_mo(self, mo_data: Dict) -> list:
        text = self._prepare_text(mo_data)
        vec = self.embedder.embed_single(text)
        return vec.tolist()

    def embed_batch(self, mos: List[Dict]) -> list:
        texts = [self._prepare_text(m) for m in mos]
        if not self.embedder.is_fitted():
            self.embedder.fit(texts)
        vecs = self.embedder.embed(texts)
        return vecs.tolist()

    def _prepare_text(self, mo: Dict) -> str:
        parts = [
            str(mo.get("description", "")),
            str(mo.get("method", "")),
            str(mo.get("target", "")),
            str(mo.get("entry_method", "")),
            str(mo.get("time_pattern", "")),
            str(mo.get("location_pattern", "")),
        ]
        return " ".join(p for p in parts if p)

    def similarity(self, mo1: Dict, mo2: Dict) -> float:
        v1 = np.array(self.embed_mo(mo1))
        v2 = np.array(self.embed_mo(mo2))
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-10))

    def find_similar(self, target: Dict, candidates: List[Dict], top_k: int = 5) -> List[Dict]:
        target_vec = np.array(self.embed_mo(target))
        results = []
        for c in candidates:
            c_vec = np.array(self.embed_mo(c))
            score = float(np.dot(target_vec, c_vec) / (np.linalg.norm(target_vec) * np.linalg.norm(c_vec) + 1e-10))
            results.append({**c, "similarity": round(score, 4)})
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
