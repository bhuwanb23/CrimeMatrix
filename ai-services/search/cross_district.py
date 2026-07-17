import json
from typing import List, Dict
import httpx
import structlog

logger = structlog.get_logger()

BACKEND_URL = "http://localhost:8001"


class CrossDistrictSearch:
    def __init__(self, backend_url: str = None):
        self.backend_url = backend_url or BACKEND_URL

    async def search(self, query: str, districts: List[str] = None,
                     top_k: int = 10) -> Dict:
        if not districts:
            districts = await self._get_all_districts()

        all_results = []
        for district in districts:
            results = await self._search_district(query, district)
            all_results.extend(results)

        seen = set()
        deduped = []
        for r in all_results:
            key = f"{r.get('entity', '')}_{r.get('id', '')}"
            if key not in seen:
                seen.add(key)
                deduped.append(r)

        return {
            "query": query,
            "districts_searched": districts,
            "total_results": len(deduped),
            "results": deduped[:top_k],
        }

    async def _get_all_districts(self) -> List[str]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.backend_url}/api/v1/districts/", timeout=10.0)
                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    items = data.get("items", data) if isinstance(data, dict) else data
                    if isinstance(items, list):
                        return [d.get("name", "") for d in items if d.get("name")]
        except Exception as e:
            logger.warning("get_districts_error", error=str(e))
        return []

    async def _search_district(self, query: str, district: str) -> List[dict]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{self.backend_url}/api/v1/search/", json={
                    "query": query,
                    "filters": [{"field": "district", "operator": "eq", "value": district}],
                }, timeout=10.0)
                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    results = data.get("results", [])
                    for r in results:
                        r["search_district"] = district
                    return results
        except Exception as e:
            logger.warning("district_search_error", district=district, error=str(e))
        return []
