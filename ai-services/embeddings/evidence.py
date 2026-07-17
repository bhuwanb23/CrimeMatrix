from typing import List, Dict
from embeddings.base import DomainEmbedder
import numpy as np
import structlog

logger = structlog.get_logger()


class EvidenceEmbeddings:
    def __init__(self):
        self.embedder = DomainEmbedder("evidence")

    def embed_evidence(self, evidence: Dict) -> list:
        text = self._prepare_text(evidence)
        vec = self.embedder.embed_single(text)
        return vec.tolist()

    def embed_batch(self, items: List[Dict]) -> list:
        texts = [self._prepare_text(e) for e in items]
        if not self.embedder.is_fitted():
            self.embedder.fit(texts)
        vecs = self.embedder.embed(texts)
        return vecs.tolist()

    def _prepare_text(self, evidence: Dict) -> str:
        parts = [
            str(evidence.get("title", "")),
            str(evidence.get("description", "")),
            str(evidence.get("type", "")),
        ]
        return " ".join(parts)

    def similarity(self, e1: Dict, e2: Dict) -> float:
        v1 = np.array(self.embed_evidence(e1))
        v2 = np.array(self.embed_evidence(e2))
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-10))
