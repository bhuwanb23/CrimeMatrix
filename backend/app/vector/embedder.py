import numpy as np
from typing import List, Dict, Optional
import structlog

logger = structlog.get_logger()


class VectorStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = None
        self.documents: List[Dict] = []
        self._init_index()

    def _init_index(self):
        try:
            import faiss
            self.index = faiss.IndexFlatL2(self.dimension)
        except ImportError:
            logger.warning("faiss_not_installed", msg="Using numpy fallback")
            self.index = None

    def _get_embedding(self, text: str) -> np.ndarray:
        # Simple hash-based embedding for demo purposes
        # In production, use sentence-transformers
        np.random.seed(hash(text) % (2**31))
        return np.random.randn(self.dimension).astype(np.float32)

    def add_document(self, doc_id: str, text: str, metadata: Dict = None):
        embedding = self._get_embedding(text)
        if self.index is not None:
            import faiss
            self.index.add(embedding.reshape(1, -1))
        self.documents.append({
            "id": doc_id,
            "text": text,
            "metadata": metadata or {},
            "embedding": embedding,
        })

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        if not self.documents:
            return []

        query_embedding = self._get_embedding(query)

        if self.index is not None and self.index.ntotal > 0:
            import faiss
            distances, indices = self.index.search(
                query_embedding.reshape(1, -1),
                min(top_k, self.index.ntotal)
            )
            results = []
            for idx in indices[0]:
                if idx < len(self.documents):
                    results.append(self.documents[idx])
            return results

        # Fallback: cosine similarity with numpy
        results = []
        for doc in self.documents:
            sim = np.dot(query_embedding, doc["embedding"]) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc["embedding"])
            )
            results.append((sim, doc))
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:top_k]]

    def get_document(self, doc_id: str) -> Optional[Dict]:
        for doc in self.documents:
            if doc["id"] == doc_id:
                return doc
        return None

    def delete_document(self, doc_id: str):
        self.documents = [d for d in self.documents if d["id"] != doc_id]

    def clear(self):
        self.documents.clear()
        self._init_index()
