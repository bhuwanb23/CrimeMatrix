import numpy as np
from typing import Dict, List, Optional
from collections import defaultdict
import structlog

logger = structlog.get_logger()


class EmbeddingStore:
    def __init__(self):
        self._store: Dict[str, Dict[str, Dict]] = defaultdict(dict)

    def add(self, domain: str, item_id: str, embedding: list, metadata: dict = None):
        self._store[domain][item_id] = {
            "embedding": np.array(embedding, dtype=np.float32),
            "metadata": metadata or {},
        }

    def get(self, domain: str, item_id: str) -> Optional[Dict]:
        entry = self._store.get(domain, {}).get(item_id)
        if entry:
            return {"id": item_id, "embedding": entry["embedding"].tolist(), **entry["metadata"]}
        return None

    def search(self, domain: str, query_embedding: list, top_k: int = 5) -> List[Dict]:
        items = self._store.get(domain, {})
        if not items:
            return []

        query_vec = np.array(query_embedding, dtype=np.float32)
        query_norm = np.linalg.norm(query_vec)
        if query_norm == 0:
            return []

        results = []
        for item_id, entry in items.items():
            item_vec = entry["embedding"]
            item_norm = np.linalg.norm(item_vec)
            if item_norm == 0:
                continue
            score = float(np.dot(query_vec, item_vec) / (query_norm * item_norm))
            results.append({
                "id": item_id,
                "score": round(score, 4),
                **entry["metadata"],
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def delete(self, domain: str, item_id: str) -> bool:
        if item_id in self._store.get(domain, {}):
            del self._store[domain][item_id]
            return True
        return False

    def clear(self, domain: str = None):
        if domain:
            self._store.pop(domain, None)
        else:
            self._store.clear()

    def get_stats(self) -> Dict:
        stats = {}
        for domain, items in self._store.items():
            if items:
                sample_vec = next(iter(items.values()))["embedding"]
                stats[domain] = {"count": len(items), "dimension": len(sample_vec)}
        return stats
