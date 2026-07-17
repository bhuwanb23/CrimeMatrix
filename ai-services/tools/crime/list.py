import json
from tools.http_tool import BackendTool


class CrimeListTool(BackendTool):
    def get_name(self) -> str:
        return "crime_list"

    def get_description(self) -> str:
        return "List all crimes with optional pagination."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "page": {"type": "integer", "description": "Page number", "default": 1},
                "per_page": {"type": "integer", "description": "Results per page", "default": 20},
            },
        }

    async def execute(self, page: int = 1, per_page: int = 20, **kwargs) -> str:
        result = await self._get(f"/api/v1/crimes/?page={page}&per_page={per_page}")
        return json.dumps(result, default=str)
