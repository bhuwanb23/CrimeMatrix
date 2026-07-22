from tools.base import Tool
import httpx
import structlog

logger = structlog.get_logger()

BACKEND_URL = "http://localhost:8001"


class RecommendationTool(Tool):
    def __init__(self, backend_url: str = None):
        self.backend_url = backend_url or BACKEND_URL

    def get_name(self) -> str:
        return "get_recommendations"

    def get_description(self) -> str:
        return (
            "Get intelligent recommendations for cases, suspects, or investigations. "
            "Combines MO patterns, location, timing, cross-district analysis, evidence review, "
            "officer assignment, priority escalation, and similarity scoring to proactively "
            "suggest actionable next steps for investigators."
        )

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "context_type": {
                    "type": "string",
                    "enum": ["dashboard", "case", "investigation"],
                    "description": "Type of recommendations: 'dashboard' for general, 'case' for case-specific, 'investigation' for investigation-specific",
                    "default": "dashboard",
                },
                "entity_id": {
                    "type": "integer",
                    "description": "Case ID or Investigation ID (required for case/investigation context)",
                },
            },
        }

    async def execute(self, context_type: str = "dashboard", entity_id: int = None, **kwargs) -> str:
        try:
            async with httpx.AsyncClient() as client:
                if context_type == "case" and entity_id:
                    url = f"{self.backend_url}/api/v1/recommendations/case/{entity_id}"
                elif context_type == "investigation" and entity_id:
                    url = f"{self.backend_url}/api/v1/recommendations/investigation/{entity_id}"
                else:
                    url = f"{self.backend_url}/api/v1/recommendations/dashboard"

                resp = await client.get(url, timeout=15.0)
                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    recs = data.get("recommendations", [])

                    if not recs:
                        return "No recommendations available at this time."

                    lines = [f"## Recommendations ({len(recs)} found)\n"]
                    type_labels = {
                        "similar_case": "Similar Case",
                        "suspect_alert": "Suspect Alert",
                        "cross_district": "Cross-District Pattern",
                        "mo_pattern": "MO Pattern Match",
                        "evidence_review": "Evidence Review",
                        "officer_assignment": "Officer Assignment",
                        "priority_escalation": "Priority Escalation",
                        "related_investigation": "Related Investigation",
                    }
                    for i, rec in enumerate(recs, 1):
                        rtype = rec.get("type", "unknown")
                        score = rec.get("score", 0)
                        label = type_labels.get(rtype, rtype.replace("_", " ").title())

                        if rtype == "similar_case":
                            lines.append(
                                f"{i}. **{label}** — {rec.get('title', 'Unknown')} "
                                f"(Score: {score}%)\n"
                                f"   Crime: {rec.get('crime_type', '?')} | "
                                f"District: {rec.get('district', '?')}\n"
                                f"   Reasons: {', '.join(rec.get('reasons', []))}"
                            )
                        elif rtype == "suspect_alert":
                            lines.append(
                                f"{i}. **{label}** — {rec.get('name', 'Unknown')} "
                                f"(Risk: {score}%)\n"
                                f"   District: {rec.get('district', '?')} | "
                                f"Status: {rec.get('status', '?')}\n"
                                f"   {rec.get('description', '')[:100]}"
                            )
                        elif rtype == "cross_district":
                            lines.append(
                                f"{i}. **{label}** — {rec.get('district', '?')}\n"
                                f"   {rec.get('message', '')}"
                            )
                        elif rtype in ("evidence_review", "officer_assignment", "priority_escalation", "related_investigation"):
                            lines.append(
                                f"{i}. **{label}** — {rec.get('title', 'Unknown')} "
                                f"(Score: {score}%)\n"
                                f"   {rec.get('description', '')}\n"
                                f"   Reasons: {', '.join(rec.get('reasons', []))}"
                            )
                        else:
                            lines.append(
                                f"{i}. **{label}** — {rec.get('title', rec.get('name', 'Unknown'))} "
                                f"(Score: {score}%)\n"
                                f"   {', '.join(rec.get('reasons', []))}"
                            )
                        lines.append("")

                    return "\n".join(lines)
                else:
                    return f"Error fetching recommendations: HTTP {resp.status_code}"
        except Exception as e:
            logger.warning("recommendation_error", error=str(e))
            return f"Error getting recommendations: {str(e)}"
