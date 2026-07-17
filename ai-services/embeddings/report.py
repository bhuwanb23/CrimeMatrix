from typing import List, Dict
from embeddings.base import DomainEmbedder
import numpy as np
import structlog

logger = structlog.get_logger()


class ReportEmbeddings:
    def __init__(self):
        self.embedder = DomainEmbedder("report")

    def embed_report(self, report: Dict) -> list:
        text = self._prepare_text(report)
        vec = self.embedder.embed_single(text)
        return vec.tolist()

    def embed_batch(self, reports: List[Dict]) -> list:
        texts = [self._prepare_text(r) for r in reports]
        if not self.embedder.is_fitted():
            self.embedder.fit(texts)
        vecs = self.embedder.embed(texts)
        return vecs.tolist()

    def _prepare_text(self, report: Dict) -> str:
        parts = [
            str(report.get("title", "")),
            str(report.get("content", "")),
            str(report.get("type", "")),
        ]
        return " ".join(parts)

    def similarity(self, r1: Dict, r2: Dict) -> float:
        v1 = np.array(self.embed_report(r1))
        v2 = np.array(self.embed_report(r2))
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-10))
