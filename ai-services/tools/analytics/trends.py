import json
from tools.http_tool import BackendTool


class AnalyticsTrendsTool(BackendTool):
    def get_name(self) -> str:
        return "analytics_trends"

    def get_description(self) -> str:
        return "Get crime trends — resolution rate, case status distribution, or crime trends over time."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "trend_type": {"type": "string", "description": "Trend type: 'resolution', 'cases', or 'crimes'", "default": "resolution"},
            },
        }

    async def execute(self, trend_type: str = "resolution", **kwargs) -> str:
        result = await self._get(f"/api/v1/analytics/trends/{trend_type}")
        return json.dumps(result, default=str)
