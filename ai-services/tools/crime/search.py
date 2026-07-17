import json
from tools.http_tool import BackendTool


class CrimeSearchTool(BackendTool):
    def get_name(self) -> str:
        return "crime_search"

    def get_description(self) -> str:
        return "Search for crimes by keyword. Returns matching crime records with details."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search keyword (e.g., 'theft', 'murder', 'bengaluru')"},
                "limit": {"type": "integer", "description": "Max results to return", "default": 10},
            },
            "required": ["query"],
        }

    async def execute(self, query: str = "", limit: int = 10, **kwargs) -> str:
        result = await self._post("/api/v1/search/", {"query": query, "limit": limit})
        return json.dumps(result, default=str)
