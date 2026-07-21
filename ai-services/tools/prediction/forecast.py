import json
from tools.base import Tool
import httpx
import structlog

logger = structlog.get_logger()
BACKEND_URL = "http://localhost:8001"


class ForecastAnalysisTool(Tool):
    def __init__(self, backend_url: str = None):
        self.backend_url = backend_url or BACKEND_URL

    def get_name(self) -> str:
        return "forecast_analysis"

    def get_description(self) -> str:
        return (
            "Analyze crime forecasts for districts or crime categories. "
            "Provides trend predictions, confidence levels, and seasonal patterns. "
            "Use when an officer asks about future crime predictions or trends."
        )

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "district_id": {"type": "integer", "description": "District ID for district-specific forecast"},
                "periods": {"type": "integer", "description": "Number of periods to forecast (default 30)", "default": 30},
            },
        }

    async def execute(self, district_id: int = None, periods: int = 30, **kwargs) -> str:
        try:
            async with httpx.AsyncClient() as client:
                if district_id:
                    resp = await client.post(f"{self.backend_url}/api/v1/predictions/forecast/district",
                        json={"district_id": district_id, "periods": periods}, timeout=20)
                else:
                    resp = await client.post(f"{self.backend_url}/api/v1/predictions/forecast",
                        json={"periods": periods}, timeout=20)

                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    trend = data.get("trend", "unknown")
                    confidence = data.get("confidence", 0)
                    forecast = data.get("forecast", [])
                    historical = data.get("historical", [])

                    lines = [
                        f"## Crime Forecast Analysis",
                        f"- **Trend:** {trend}",
                        f"- **Confidence:** {confidence}%",
                        f"- **Data points:** {data.get('data_points', 0)}",
                        "",
                    ]
                    if forecast:
                        lines.append("### Predicted Values:")
                        for f in forecast[:5]:
                            lines.append(f"- {f.get('date', 'N/A')}: {f.get('predicted', 0)} crimes")
                    if district_id and data.get("district"):
                        lines.append(f"\n**District:** {data['district'].get('name', 'Unknown')}")

                    return "\n".join(lines)
                return f"Error: HTTP {resp.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
