import json
from tools.base import Tool
import httpx
import structlog

logger = structlog.get_logger()
BACKEND_URL = "http://localhost:8001"


class RiskAssessmentTool(Tool):
    def get_name(self) -> str:
        return "risk_assessment"

    def get_description(self) -> str:
        return (
            "Assess risk levels for suspects. Provides explainable risk scores "
            "with contributing factors, risk history, and recommendations. "
            "Use when an officer asks why a suspect is considered high risk."
        )

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "suspect_id": {"type": "integer", "description": "Suspect ID to assess"},
                "action": {"type": "string", "enum": ["score", "rankings", "factors"], "default": "rankings"},
            },
        }

    async def execute(self, suspect_id: int = None, action: str = "rankings", **kwargs) -> str:
        try:
            async with httpx.AsyncClient() as client:
                if action == "score" and suspect_id:
                    resp = await client.post(f"{self.backend_url}/api/v1/suspect-risk/score/{suspect_id}", timeout=20)
                elif action == "factors" and suspect_id:
                    resp = await client.get(f"{self.backend_url}/api/v1/suspect-risk/factors/{suspect_id}", timeout=15)
                else:
                    resp = await client.get(f"{self.backend_url}/api/v1/suspect-risk/rankings?limit=10", timeout=15)

                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    if action == "rankings" and isinstance(data, list):
                        lines = ["## Suspect Risk Rankings\n"]
                        for i, r in enumerate(data[:10], 1):
                            lines.append(f"{i}. **{r.get('name', 'Unknown')}** — Risk: {r.get('overall_score', 0)}% ({r.get('risk_level', 'unknown')})")
                        return "\n".join(lines) if lines else "No risk data available."
                    elif action == "score" and isinstance(data, dict):
                        return f"**Risk Score:** {data.get('overall_score', 0)}% ({data.get('risk_level', 'unknown')})\n\n**Explanation:**\n" + "\n".join(f"- {e}" for e in data.get("explanation", []))
                    elif action == "factors" and isinstance(data, dict):
                        items = data.get("items", [])
                        lines = ["## Risk Factors\n"]
                        for f in items:
                            lines.append(f"- **{f.get('name', '')}**: {f.get('value', 0)}% (weight: {f.get('weight', 0)})")
                        return "\n".join(lines) if lines else "No risk factors found."
                    return json.dumps(data, default=str)[:500]
                return f"Error: HTTP {resp.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
