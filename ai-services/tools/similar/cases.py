from typing import Dict, Any
from tools.base import Tool
import httpx
import structlog

logger = structlog.get_logger()

BACKEND_URL = "http://localhost:8001"


class SimilarCasesTool(Tool):
    def __init__(self, backend_url: str = None):
        self.backend_url = backend_url or BACKEND_URL

    def get_name(self) -> str:
        return "similar_cases"

    def get_description(self) -> str:
        return (
            "Find cases similar to a given case. Compares modus operandi (MO), "
            "location, timing, suspects, evidence, and vehicles to identify "
            "related crimes. Returns ranked similar cases with per-dimension "
            "similarity scores and human-readable reasons."
        )

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "case_id": {
                    "type": "integer",
                    "description": "The ID of the case to find similar cases for",
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of similar cases to return (default 5, max 20)",
                    "default": 5,
                },
            },
            "required": ["case_id"],
        }

    async def execute(self, case_id: int, top_k: int = 5, **kwargs) -> str:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.backend_url}/api/v1/similar-cases/{case_id}",
                    params={"top_k": min(top_k, 20)},
                    timeout=15.0,
                )
                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    similar = data.get("similar_cases", [])

                    if not similar:
                        return f"No similar cases found for case #{case_id}."

                    lines = [f"Found {len(similar)} similar cases for case #{case_id}:\n"]
                    for i, s in enumerate(similar, 1):
                        score = s.get("overall_score", 0)
                        lines.append(
                            f"{i}. **{s.get('case_number', 'N/A')}** — {s.get('title', 'Unknown')}\n"
                            f"   Type: {s.get('crime_type', '?')} | District: {s.get('district', '?')} | Status: {s.get('status', '?')}\n"
                            f"   Overall Match: {score}%\n"
                            f"   MO: {s.get('mo_score', 0)}% | Location: {s.get('location_score', 0)}% | "
                            f"Time: {s.get('time_score', 0)}% | Suspects: {s.get('suspects_score', 0)}% | "
                            f"Evidence: {s.get('evidence_score', 0)}% | Vehicles: {s.get('vehicles_score', 0)}%"
                        )
                        reasons = s.get("reasons", [])
                        if reasons:
                            lines.append(f"   Reasons: {', '.join(reasons)}")
                        lines.append("")

                    return "\n".join(lines)
                else:
                    return f"Error fetching similar cases: HTTP {resp.status_code}"
        except Exception as e:
            logger.warning("similar_cases_error", case_id=case_id, error=str(e))
            return f"Error finding similar cases: {str(e)}"
