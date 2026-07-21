import json
from tools.base import Tool
import httpx
import structlog

logger = structlog.get_logger()
BACKEND_URL = "http://localhost:8001"


class PriorityAnalysisTool(Tool):
    def get_name(self) -> str:
        return "priority_analysis"

    def get_description(self) -> str:
        return (
            "Analyze investigation priorities. Provides priority scores, "
            "explanations, workload overview, and suggested actions. "
            "Use when an officer asks which cases to investigate first."
        )

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "investigation_id": {"type": "integer", "description": "Investigation ID to analyze"},
                "action": {"type": "string", "enum": ["rankings", "explain", "workload", "score"], "default": "rankings"},
            },
        }

    async def execute(self, investigation_id: int = None, action: str = "rankings", **kwargs) -> str:
        try:
            async with httpx.AsyncClient() as client:
                if action == "score" and investigation_id:
                    resp = await client.post(f"{self.backend_url}/api/v1/priorities/score/{investigation_id}", timeout=20)
                elif action == "explain" and investigation_id:
                    resp = await client.get(f"{self.backend_url}/api/v1/priorities/explain/{investigation_id}", timeout=15)
                elif action == "workload":
                    resp = await client.get(f"{self.backend_url}/api/v1/priorities/workload", timeout=15)
                else:
                    resp = await client.get(f"{self.backend_url}/api/v1/priorities/rankings?limit=10", timeout=15)

                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    if action == "rankings" and isinstance(data, list):
                        lines = ["## Investigation Priority Queue\n"]
                        for i, r in enumerate(data[:10], 1):
                            lines.append(f"{i}. **{r.get('title', 'Unknown')}** — Priority: {r.get('overall_score', 0)}% ({r.get('priority_level', 'unknown')})")
                        return "\n".join(lines) if lines else "No priority data available."
                    elif action == "explain" and isinstance(data, dict):
                        items = data.get("items", [])
                        lines = ["## Priority Explanation\n"]
                        for e in items:
                            lines.append(f"- **{e.get('factor', '')}**: {e.get('score', 0)}% — {e.get('explanation', '')}")
                        return "\n".join(lines) if lines else "No explanations available."
                    elif action == "workload" and isinstance(data, list):
                        lines = ["## Officer Workload\n"]
                        for w in data:
                            lines.append(f"- Officer #{w.get('officer_id', '?')}: {w.get('count', 0)} cases ({w.get('high_priority', 0)} high priority)")
                        return "\n".join(lines) if lines else "No workload data."
                    elif action == "score" and isinstance(data, dict):
                        return f"**Priority Score:** {data.get('overall_score', 0)}% ({data.get('priority_level', 'unknown')})\n\n**Factors:**\n" + "\n".join(f"- {e.get('factor', '')}: {e.get('score', 0)}%" for e in data.get("explanations", []))
                    return json.dumps(data, default=str)[:500]
                return f"Error: HTTP {resp.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
