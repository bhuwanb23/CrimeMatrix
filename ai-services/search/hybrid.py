import numpy as np
from typing import List, Optional
from rag.vector_store import VectorStore
from rag.embeddings import EmbeddingGenerator
import structlog

logger = structlog.get_logger()


class HybridSearch:
    def __init__(self, vector_store: VectorStore = None,
                 weight_keyword: float = 0.3, weight_semantic: float = 0.7):
        self.vector_store = vector_store or VectorStore()
        self.weight_keyword = weight_keyword
        self.weight_semantic = weight_semantic
        self.embedder = self.vector_store.embedder

    def _keyword_score(self, query: str, content: str) -> float:
        query_terms = set(query.lower().split())
        content_lower = content.lower()
        if not query_terms:
            return 0.0
        matches = sum(1 for t in query_terms if t in content_lower)
        return matches / len(query_terms)

    def search(self, query: str, top_k: int = 5, doc_type: str = None) -> List[dict]:
        if not self.vector_store._indexed or not self.vector_store._chunks:
            return []

        query_vec = self.embedder.embed_single(query)
        semantic_scores = np.dot(self.vector_store._vectors, query_vec) / (
            np.linalg.norm(self.vector_store._vectors, axis=1) * np.linalg.norm(query_vec) + 1e-10
        )

        max_sem = max(semantic_scores) if len(semantic_scores) > 0 else 1.0
        if max_sem > 0:
            semantic_scores = semantic_scores / max_sem

        results = []
        for i, chunk in enumerate(self.vector_store._chunks):
            if doc_type and chunk.get("doc_type") != doc_type:
                continue
            kw_score = self._keyword_score(query, chunk.get("content", ""))
            sem_score = float(semantic_scores[i])
            hybrid_score = (self.weight_keyword * kw_score) + (self.weight_semantic * sem_score)
            results.append({**chunk, "score": hybrid_score, "keyword_score": kw_score, "semantic_score": sem_score})

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
