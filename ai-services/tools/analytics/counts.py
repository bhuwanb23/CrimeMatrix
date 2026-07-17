import json
from tools.http_tool import BackendTool


class AnalyticsCountsTool(BackendTool):
    def get_name(self) -> str:
        return "analytics_counts"

    def get_description(self) -> str:
        return "Get crime counts broken down by type, status, district, or priority."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "by": {"type": "string", "description": "Group by: 'type', 'status', 'district', or 'priority'", "default": "type"},
            },
        }

    async def execute(self, by: str = "type", **kwargs) -> str:
        result = await self._get(f"/api/v1/analytics/counts/by-{by}")
        return json.dumps(result, default=str)
