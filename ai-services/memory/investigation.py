import httpx
from typing import Dict, Any, Optional
import structlog

logger = structlog.get_logger()

BACKEND_URL = "http://localhost:8001"


class InvestigationContext:
    def __init__(self, backend_url: str = None):
        self.backend_url = backend_url or BACKEND_URL
        self._cache: Dict[str, dict] = {}

    async def load_investigation(self, investigation_id: int) -> Optional[Dict]:
        cache_key = f"investigation_{investigation_id}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}/api/v1/crimes/{investigation_id}", timeout=10.0)
                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    self._cache[cache_key] = data
                    return data
        except Exception as e:
            logger.warning("investigation_load_error", id=investigation_id, error=str(e))
        return None

    async def load_crime(self, crime_id: int) -> Optional[Dict]:
        cache_key = f"crime_{crime_id}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}/api/v1/crimes/{crime_id}", timeout=10.0)
                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    self._cache[cache_key] = data
                    return data
        except Exception as e:
            logger.warning("crime_load_error", id=crime_id, error=str(e))
        return None

    async def load_suspect(self, suspect_id: int) -> Optional[Dict]:
        cache_key = f"suspect_{suspect_id}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}/api/v1/criminals/{suspect_id}", timeout=10.0)
                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    self._cache[cache_key] = data
                    return data
        except Exception as e:
            logger.warning("suspect_load_error", id=suspect_id, error=str(e))
        return None

    def format_for_context(self, data: Dict, entity_type: str = "crime") -> str:
        if not data:
            return "No data loaded."
        lines = [f"## {entity_type.title()} Context"]
        for k, v in data.items():
            if v and k not in ("id", "created_at", "updated_at"):
                lines.append(f"- {k}: {str(v)[:300]}")
        return "\n".join(lines)

    def clear_cache(self):
        self._cache.clear()
