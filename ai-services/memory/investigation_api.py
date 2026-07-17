import httpx
from typing import Dict, List, Optional
import structlog

logger = structlog.get_logger()

BACKEND_URL = "http://localhost:8001"


class InvestigationContextAPI:
    def __init__(self, backend_url: str = None):
        self.backend_url = backend_url or BACKEND_URL

    async def get_case(self, case_id: int) -> Optional[Dict]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}/api/v1/crimes/{case_id}", timeout=10.0)
                if resp.status_code == 200:
                    return resp.json().get("data", {})
        except Exception as e:
            logger.warning("get_case_error", error=str(e))
        return None

    async def get_investigation(self, investigation_id: int) -> Optional[Dict]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}/api/v1/crimes/{investigation_id}", timeout=10.0)
                if resp.status_code == 200:
                    return resp.json().get("data", {})
        except Exception as e:
            logger.warning("get_investigation_error", error=str(e))
        return None

    async def search_cases(self, query: str, limit: int = 10) -> List[Dict]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{self.backend_url}/api/v1/search/", json={"query": query, "limit": limit}, timeout=10.0)
                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    return data.get("results", []) if isinstance(data, dict) else data
        except Exception as e:
            logger.warning("search_cases_error", error=str(e))
        return []

    async def get_suspects(self, limit: int = 10) -> List[Dict]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}/api/v1/criminals/?limit={limit}", timeout=10.0)
                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    return data.get("items", data) if isinstance(data, dict) else data
        except Exception as e:
            logger.warning("get_suspects_error", error=str(e))
        return []

    async def get_notes(self, investigation_id: int) -> List[Dict]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}/api/v1/notes/?investigation_id={investigation_id}", timeout=10.0)
                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    return data.get("items", data) if isinstance(data, dict) else data
        except Exception as e:
            logger.warning("get_notes_error", error=str(e))
        return []

    async def get_statistics(self) -> Dict:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}/api/v1/analytics/stats/overview", timeout=10.0)
                if resp.status_code == 200:
                    return resp.json().get("data", {})
        except Exception as e:
            logger.warning("get_statistics_error", error=str(e))
        return {}

    def format_case_context(self, case: Dict) -> str:
        if not case:
            return ""
        lines = [f"## Active Case: {case.get('title', 'Unknown')}"]
        lines.append(f"- Status: {case.get('status', 'unknown')}")
        lines.append(f"- Priority: {case.get('priority', 'medium')}")
        if case.get("description"):
            lines.append(f"- Description: {case['description'][:500]}")
        if case.get("crime_type"):
            lines.append(f"- Crime Type: {case['crime_type']}")
        if case.get("district"):
            lines.append(f"- District: {case['district']}")
        return "\n".join(lines)
