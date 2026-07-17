import numpy as np
from typing import List, Dict, Optional
from rag.embeddings import EmbeddingGenerator
import structlog

logger = structlog.get_logger()


class VectorStore:
    def __init__(self):
        self.embedder = EmbeddingGenerator()
        self._chunks: List[dict] = []
        self._vectors: Optional[np.ndarray] = None
        self._indexed = False

    def add_chunks(self, chunks: List[dict]):
        self._chunks.extend(chunks)
        texts = [c["content"] for c in self._chunks]
        self.embedder.fit(texts)
        self._vectors = self.embedder.embed(texts)
        self._indexed = True
        logger.info("vector_store_updated", total_chunks=len(self._chunks))

    def search(self, query: str, top_k: int = 5, doc_type: str = None) -> List[dict]:
        if not self._indexed or not self._chunks:
            return []

        query_vec = self.embedder.embed_single(query)
        similarities = np.dot(self._vectors, query_vec) / (
            np.linalg.norm(self._vectors, axis=1) * np.linalg.norm(query_vec) + 1e-10
        )

        ranked_indices = np.argsort(similarities)[::-1]

        results = []
        for idx in ranked_indices:
            if len(results) >= top_k:
                break
            chunk = self._chunks[idx]
            if doc_type and chunk.get("doc_type") != doc_type:
                continue
            results.append({
                **chunk,
                "score": float(similarities[idx]),
            })
        return results

    def get_all_chunks(self) -> List[dict]:
        return self._chunks

    def get_stats(self) -> dict:
        types = {}
        for c in self._chunks:
            t = c.get("doc_type", "unknown")
            types[t] = types.get(t, 0) + 1
        return {
            "total_chunks": len(self._chunks),
            "indexed": self._indexed,
            "doc_types": types,
        }

    def clear(self):
        self._chunks.clear()
        self._vectors = None
        self._indexed = False
