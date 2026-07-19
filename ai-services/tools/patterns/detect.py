from tools.base import Tool
import httpx
import structlog

logger = structlog.get_logger()

BACKEND_URL = "http://localhost:8001"


class PatternDetectTool(Tool):
    def __init__(self, backend_url: str = None):
        self.backend_url = backend_url or BACKEND_URL

    def get_name(self) -> str:
        return "detect_patterns"

    def get_description(self) -> str:
        return (
            "Detect recurring crime patterns by analyzing MO, timing, location, "
            "and crime type clusters. Identifies patterns like 'burglaries at night' "
            "or 'thefts near railway stations'. Triggers pattern detection on all "
            "crime data and returns discovered patterns."
        )

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "crime_type": {
                    "type": "string",
                    "description": "Filter detection to specific crime type (optional)",
                },
                "district": {
                    "type": "string",
                    "description": "Filter detection to specific district (optional)",
                },
            },
        }

    async def execute(self, crime_type: str = None, district: str = None, **kwargs) -> str:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{self.backend_url}/api/v1/patterns/detect",
                    timeout=30.0,
                )
                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    total = data.get("patterns_found", 0)
                    saved = data.get("patterns_saved", 0)

                    lines = [
                        f"## Pattern Detection Results",
                        f"",
                        f"**Patterns discovered:** {total}",
                        f"**New patterns saved:** {saved}",
                        f"",
                        f"### Breakdown",
                        f"- Time patterns: {data.get('time_patterns', 0)}",
                        f"- MO patterns: {data.get('mo_patterns', 0)}",
                        f"- Location patterns: {data.get('location_patterns', 0)}",
                    ]

                    if total == 0:
                        lines.append("")
                        lines.append("No significant patterns detected. Need more crime data for pattern analysis.")

                    return "\n".join(lines)
                else:
                    return f"Error detecting patterns: HTTP {resp.status_code}"
        except Exception as e:
            logger.warning("pattern_detect_error", error=str(e))
            return f"Error detecting patterns: {str(e)}"
