import json
from tools.http_tool import BackendTool


class CrimeSearchTool(BackendTool):
    def get_name(self) -> str:
        return "crime_search"

    def get_description(self) -> str:
        return "Search for crimes by keyword and optional filters (crime_type, district, status, priority, date_from, date_to)."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search keyword"},
                "crime_type": {"type": "string", "description": "Filter by crime type (theft, murder, robbery, etc.)"},
                "district": {"type": "string", "description": "Filter by district (Bengaluru, Mysore, etc.)"},
                "status": {"type": "string", "description": "Filter by status (open, closed, pending)"},
                "priority": {"type": "string", "description": "Filter by priority (high, medium, low)"},
                "date_from": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                "date_to": {"type": "string", "description": "End date (YYYY-MM-DD)"},
                "limit": {"type": "integer", "description": "Max results", "default": 10},
            },
            "required": ["query"],
        }

    async def execute(self, query: str = "", crime_type: str = None, district: str = None,
                      status: str = None, priority: str = None, date_from: str = None,
                      date_to: str = None, limit: int = 10, **kwargs) -> str:
        filters = []
        if crime_type:
            filters.append({"field": "crime_type", "operator": "like", "value": crime_type})
        if district:
            filters.append({"field": "district", "operator": "like", "value": district})
        if status:
            filters.append({"field": "status", "operator": "eq", "value": status})
        if priority:
            filters.append({"field": "priority", "operator": "eq", "value": priority})

        payload = {"query": query, "limit": limit}
        if filters:
            payload["filters"] = filters

        result = await self._post("/api/v1/search/", payload)
        return json.dumps(result, default=str)
