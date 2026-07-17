import json
from tools.http_tool import BackendTool


class CrimeDetailTool(BackendTool):
    def get_name(self) -> str:
        return "crime_detail"

    def get_description(self) -> str:
        return "Get full details of a specific crime by its ID."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "crime_id": {"type": "integer", "description": "The crime ID"},
            },
            "required": ["crime_id"],
        }

    async def execute(self, crime_id: int = 0, **kwargs) -> str:
        result = await self._get(f"/api/v1/crimes/{crime_id}")
        return json.dumps(result, default=str)
