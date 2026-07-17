import httpx
import json
from tools.base import Tool
import structlog

logger = structlog.get_logger()

BACKEND_URL = "http://localhost:8001"


class BackendTool(Tool):
    def __init__(self, base_url: str = None):
        self.base_url = base_url or BACKEND_URL

    async def _get(self, path: str) -> dict:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.base_url}{path}", timeout=10.0)
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            logger.error("backend_get_error", path=path, error=str(e))
            return {"error": str(e)}

    async def _post(self, path: str, data: dict = None) -> dict:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{self.base_url}{path}", json=data or {}, timeout=10.0)
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            logger.error("backend_post_error", path=path, error=str(e))
            return {"error": str(e)}
