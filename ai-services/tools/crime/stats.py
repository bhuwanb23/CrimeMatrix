import json
from tools.http_tool import BackendTool


class CrimeStatsTool(BackendTool):
    def get_name(self) -> str:
        return "crime_stats"

    def get_description(self) -> str:
        return "Get overall crime statistics — total crimes, persons, officers, resolution rate."

    def get_parameters(self) -> dict:
        return {"type": "object", "properties": {}}

    async def execute(self, **kwargs) -> str:
        result = await self._get("/api/v1/analytics/stats/overview")
        return json.dumps(result, default=str)
