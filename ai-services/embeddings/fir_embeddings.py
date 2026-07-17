from typing import List, Dict
from embeddings.base import DomainEmbedder
import numpy as np
import structlog

logger = structlog.get_logger()


class FIREmbeddings:
    def __init__(self):
        self.embedder = DomainEmbedder("fir")

    def embed_fir(self, fir_data: Dict) -> list:
        text = self._prepare_text(fir_data)
        vec = self.embedder.embed_single(text)
        return vec.tolist()

    def embed_batch(self, firs: List[Dict]) -> list:
        texts = [self._prepare_text(f) for f in firs]
        if not self.embedder.is_fitted():
            self.embedder.fit(texts)
        vecs = self.embedder.embed(texts)
        return vecs.tolist()

    def _prepare_text(self, fir: Dict) -> str:
        parts = [
            str(fir.get("title", "")),
            str(fir.get("description", "")),
            str(fir.get("crime_type", "")),
            str(fir.get("district", "")),
            str(fir.get("status", "")),
        ]
        return " ".join(parts)

    def similarity(self, fir1: Dict, fir2: Dict) -> float:
        v1 = self.embed_fir(fir1)
        v2 = self.embed_fir(fir2)
        a, b = np.array(v1), np.array(v2)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))
