from tools.base import Tool
import httpx
import structlog

logger = structlog.get_logger()

BACKEND_URL = "http://localhost:8001"


class ExplainInsightTool(Tool):
    def __init__(self, backend_url: str = None):
        self.backend_url = backend_url or BACKEND_URL

    def get_name(self) -> str:
        return "explain_insight"

    def get_description(self) -> str:
        return (
            "Explain why an alert, recommendation, or evidence link was generated. "
            "Provides detailed reasoning chain, confidence score, and supporting evidence "
            "for any proactive intelligence insight. Use this when an officer asks "
            "'Why was this alert generated?', 'Why was this evidence linked?', or "
            "'Explain this recommendation'."
        )

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "context_type": {
                    "type": "string",
                    "enum": ["event", "recommendation", "evidence_link", "alert"],
                    "description": "Type of insight to explain: 'event' for intelligence events, 'recommendation' for recommendation recs, 'evidence_link' for evidence links, 'alert' for early warning alerts",
                },
                "entity_id": {
                    "type": "integer",
                    "description": "ID of the entity to explain (event ID, recommendation ID, link ID, or alert ID)",
                },
            },
            "required": ["context_type", "entity_id"],
        }

    async def execute(self, context_type: str = "event", entity_id: int = 0, **kwargs) -> str:
        try:
            endpoint_map = {
                "event": f"/api/v1/proactive/explain/event/{entity_id}",
                "recommendation": f"/api/v1/proactive/explain/recommendation/{entity_id}",
                "evidence_link": f"/api/v1/proactive/explain/evidence-link/{entity_id}",
                "alert": f"/api/v1/proactive/explain/alert/{entity_id}",
            }

            url = f"{self.backend_url}{endpoint_map.get(context_type, endpoint_map['event'])}"

            async with httpx.AsyncClient() as client:
                resp = await client.post(url, timeout=15.0)

            if resp.status_code == 200:
                data = resp.json().get("data", {})
                return self._format_explanation(data, context_type, entity_id)
            else:
                return f"Error fetching explanation: HTTP {resp.status_code}"

        except Exception as e:
            logger.warning("explain_insight_error", error=str(e))
            return f"Error generating explanation: {str(e)}"

    def _format_explanation(self, data: dict, context_type: str, entity_id: int) -> str:
        lines = []

        confidence = data.get("confidence", {})
        conf_score = confidence.get("score", 0)
        conf_level = confidence.get("level", "unknown")

        lines.append(f"## AI Explanation ({context_type} #{entity_id})")
        lines.append(f"**Confidence:** {conf_score}% ({conf_level.upper()})")
        lines.append("")

        explanation = data.get("explanation", "No explanation available.")
        lines.append(f"### Summary")
        lines.append(explanation)
        lines.append("")

        chain = data.get("reasoning_chain", [])
        if chain:
            lines.append("### Reasoning Chain")
            for step in chain:
                step_num = step.get("step", "?")
                claim = step.get("claim", "")
                etype = step.get("evidence_type", "")
                conf = step.get("confidence", 0)
                lines.append(f"{step_num}. **{etype}** — {claim} (confidence: {conf}%)")
            lines.append("")

        evidence = data.get("supporting_evidence", [])
        if evidence:
            lines.append("### Supporting Evidence")
            for ev in evidence:
                ev_type = ev.get("type", "")
                desc = ev.get("description", "")
                strength = ev.get("strength", 0)
                pct = round(strength * 100) if strength <= 1 else round(strength)
                lines.append(f"- **{ev_type}**: {desc} ({pct}% strength)")
            lines.append("")

        actions = data.get("recommended_actions", [])
        if actions:
            lines.append("### Recommended Actions")
            for a in actions:
                lines.append(f"- {a}")

        return "\n".join(lines)
