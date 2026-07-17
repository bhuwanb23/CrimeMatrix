import json
from tools.http_tool import BackendTool


class GraphShortestPathTool(BackendTool):
    def get_name(self) -> str:
        return "graph_shortest"

    def get_description(self) -> str:
        return "Find the shortest path between two nodes in the graph."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Source node ID"},
                "target": {"type": "string", "description": "Target node ID"},
            },
            "required": ["source", "target"],
        }

    async def execute(self, source: str = "", target: str = "", **kwargs) -> str:
        result = await self._get(f"/api/v1/graph/shortest/{source}/{target}")
        return json.dumps(result, default=str)
