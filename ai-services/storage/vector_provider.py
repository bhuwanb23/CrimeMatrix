import numpy as np
from typing import Dict, List, Optional
from collections import defaultdict
from storage.base import VectorProvider
from models.embedding import EmbeddingModel
import structlog

logger = structlog.get_logger()


class VectorProvider(VectorProvider):
    def __init__(self):
        self._store: Dict[str, Dict[str, Dict]] = defaultdict(dict)
        self._embedder = EmbeddingModel()

    async def connect(self):
        logger.info("vector_provider_connected")

    async def disconnect(self):
        pass

    async def add(self, collection: str, item_id: str, vector: list, metadata: dict = None):
        self._store[collection][item_id] = {
            "vector": np.array(vector, dtype=np.float32),
            "metadata": metadata or {},
        }

    async def search(self, collection: str, query_vector: list, top_k: int = 5) -> List[Dict]:
        items = self._store.get(collection, {})
        if not items:
            return []
        query_vec = np.array(query_vector, dtype=np.float32)
        query_norm = np.linalg.norm(query_vec)
        if query_norm == 0:
            return []
        results = []
        for item_id, entry in items.items():
            item_vec = entry["vector"]
            item_norm = np.linalg.norm(item_vec)
            if item_norm == 0:
                continue
            score = float(np.dot(query_vec, item_vec) / (query_norm * item_norm))
            results.append({"id": item_id, "score": round(score, 4), **entry["metadata"]})
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    async def get(self, collection: str, item_id: str) -> Optional[Dict]:
        entry = self._store.get(collection, {}).get(item_id)
        if entry:
            return {"id": item_id, "vector": entry["vector"].tolist(), **entry["metadata"]}
        return None

    async def delete(self, collection: str, item_id: str) -> bool:
        if item_id in self._store.get(collection, {}):
            del self._store[collection][item_id]
            return True
        return False

    async def count(self, collection: str) -> int:
        return len(self._store.get(collection, {}))

    async def list_collections(self) -> List[str]:
        return [c for c, items in self._store.items() if items]

    async def clear(self, collection: str):
        self._store.pop(collection, None)
