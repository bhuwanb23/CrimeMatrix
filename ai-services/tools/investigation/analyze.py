import json
from tools.base import Tool
import httpx
import structlog

logger = structlog.get_logger()

BACKEND_URL = "http://localhost:8001"


class InvestigationAnalyzeTool(Tool):
    def __init__(self, backend_url: str = None):
        self.backend_url = backend_url or BACKEND_URL

    def get_name(self) -> str:
        return "investigation_analyze"

    def get_description(self) -> str:
        return (
            "Perform comprehensive investigation analysis. Can summarize findings, "
            "suggest leads, review evidence, find similar crimes, or generate a full "
            "investigation report. Use this tool when the officer asks about an "
            "investigation — it gathers all relevant data and produces structured analysis."
        )

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "investigation_id": {
                    "type": "integer",
                    "description": "The ID of the investigation to analyze",
                },
                "analysis_type": {
                    "type": "string",
                    "enum": ["summary", "leads", "evidence", "similar", "full"],
                    "description": (
                        "Type of analysis: 'summary' for overview, 'leads' for suggested "
                        "next steps, 'evidence' for evidence review, 'similar' for related "
                        "cases, 'full' for comprehensive report"
                    ),
                    "default": "summary",
                },
                "question": {
                    "type": "string",
                    "description": "Optional specific question about the investigation",
                },
            },
            "required": ["investigation_id"],
        }

    async def execute(self, investigation_id: int, analysis_type: str = "summary",
                      question: str = None, **kwargs) -> str:
        try:
            async with httpx.AsyncClient() as client:
                payload = {"analysis_type": analysis_type}
                if question:
                    payload["question"] = question

                resp = await client.post(
                    f"{self.backend_url}/api/v1/investigations/{investigation_id}/analyze",
                    json=payload,
                    timeout=20.0,
                )
                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    context = data.get("context", "")
                    meta = data.get("data", {})

                    if not context:
                        return f"No analysis data available for investigation #{investigation_id}."

                    lines = [context]
                    if meta:
                        lines.append(f"\n---")
                        lines.append(f"Analysis type: {meta.get('analysis_type', 'summary')}")
                        lines.append(f"Notes: {meta.get('notes_count', 0)} | Evidence: {meta.get('evidence_count', 0)} | Timeline: {meta.get('timeline_count', 0)} | Similar: {meta.get('similar_count', 0)}")

                    return "\n".join(lines)
                else:
                    return f"Error analyzing investigation: HTTP {resp.status_code}"
        except Exception as e:
            logger.warning("investigation_analyze_error", investigation_id=investigation_id, error=str(e))
            return f"Error analyzing investigation: {str(e)}"
