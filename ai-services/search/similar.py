import json
from typing import List, Dict, Optional
from rag.vector_store import VectorStore
import httpx
import structlog

logger = structlog.get_logger()

BACKEND_URL = "http://localhost:8001"


class SimilarCaseSearch:
    def __init__(self, vector_store: VectorStore = None, backend_url: str = None):
        self.vector_store = vector_store or VectorStore()
        self.backend_url = backend_url or BACKEND_URL

    async def find_similar(self, case_id: int, top_k: int = 5) -> List[dict]:
        case = await self._load_case(case_id)
        if not case:
            return []

        query = f"{case.get('title', '')} {case.get('description', '')} {case.get('crime_type', '')}"
        results = self.vector_store.search(query, top_k=top_k + 1)

        similar = []
        for r in results:
            doc_id = r.get("doc_id", "")
            if doc_id.endswith(str(case_id)):
                continue
            similar.append({
                "doc_id": doc_id,
                "content": r.get("content", "")[:300],
                "score": r.get("score", 0),
                "source": r.get("source", ""),
                "doc_type": r.get("doc_type", ""),
            })
            if len(similar) >= top_k:
                break
        return similar

    async def _load_case(self, case_id: int) -> Optional[dict]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}/api/v1/crimes/{case_id}", timeout=10.0)
                if resp.status_code == 200:
                    return resp.json().get("data", {})
        except Exception as e:
            logger.warning("load_case_error", case_id=case_id, error=str(e))
        return None
