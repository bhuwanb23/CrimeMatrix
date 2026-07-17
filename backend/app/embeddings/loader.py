import json
import numpy as np
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.embeddings.persistence import VectorPersistence
import structlog

logger = structlog.get_logger()


class VectorLoader:
    def __init__(self, db: AsyncSession):
        self.persistence = VectorPersistence(db)
        self._chunks: List[Dict] = []
        self._vectors: Optional[np.ndarray] = None

    async def load(self, domain: str = None) -> Dict:
        if domain:
            self._chunks = await self.persistence.get_chunks_by_domain(domain)
        else:
            self._chunks = await self.persistence.get_all_chunks()

        if self._chunks:
            vectors = np.array([c["vector"] for c in self._chunks], dtype=np.float32)
            self._vectors = vectors
        else:
            self._vectors = None

        stats = {"chunks_loaded": len(self._chunks), "has_vectors": self._vectors is not None}
        logger.info("vectors_loaded", **stats)
        return stats

    def search(self, query_vector: list, top_k: int = 5) -> List[Dict]:
        if not self._chunks or self._vectors is None:
            return []

        query_vec = np.array(query_vector, dtype=np.float32)
        query_norm = np.linalg.norm(query_vec)
        if query_norm == 0:
            return []

        similarities = np.dot(self._vectors, query_vec) / (
            np.linalg.norm(self._vectors, axis=1) * query_norm + 1e-10
        )

        ranked_indices = np.argsort(similarities)[::-1][:top_k]
        results = []
        for idx in ranked_indices:
            chunk = self._chunks[idx]
            results.append({
                "chunk_id": chunk.get("chunk_id"),
                "document_id": chunk.get("document_id"),
                "content": chunk["content"],
                "domain": chunk.get("domain"),
                "score": round(float(similarities[idx]), 4),
                "metadata": chunk.get("metadata", {}),
            })
        return results

    def get_stats(self) -> Dict:
        return {
            "total_chunks": len(self._chunks),
            "has_vectors": self._vectors is not None,
            "vector_dimension": int(self._vectors.shape[1]) if self._vectors is not None else 0,
        }
