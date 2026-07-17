import httpx
from typing import Dict, List, Optional
import structlog

logger = structlog.get_logger()

BACKEND_URL = "http://localhost:8001"


class EmbeddingPersistenceClient:
    def __init__(self, backend_url: str = None):
        self.backend_url = backend_url or BACKEND_URL

    async def save(self, domain: str, item_id: str, content: str,
                    vector: list, metadata: dict = None, source: str = "unknown") -> bool:
        try:
            async with httpx.AsyncClient() as client:
                data = {"domain": domain, "item_id": item_id, "content": content,
                        "vector": vector, "metadata": metadata or {}, "source": source}
                resp = await client.post(f"{self.backend_url}/api/v1/embeddings/save", json=data, timeout=10.0)
                return resp.status_code == 200
        except Exception as e:
            logger.warning("embedding_save_error", error=str(e))
        return False

    async def load_all(self, domain: str = None) -> List[Dict]:
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.backend_url}/api/v1/embeddings/load"
                if domain:
                    url += f"?domain={domain}"
                resp = await client.get(url, timeout=10.0)
                if resp.status_code == 200:
                    return resp.json().get("data", [])
        except Exception as e:
            logger.warning("embedding_load_error", error=str(e))
        return []

    async def delete(self, doc_id: int) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.delete(f"{self.backend_url}/api/v1/embeddings/{doc_id}", timeout=10.0)
                return resp.status_code == 200
        except Exception as e:
            logger.warning("embedding_delete_error", error=str(e))
        return False

    async def count(self, domain: str = None) -> int:
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.backend_url}/api/v1/embeddings/count"
                if domain:
                    url += f"?domain={domain}"
                resp = await client.get(url, timeout=10.0)
                if resp.status_code == 200:
                    return resp.json().get("data", {}).get("count", 0)
        except Exception as e:
            logger.warning("embedding_count_error", error=str(e))
        return 0
