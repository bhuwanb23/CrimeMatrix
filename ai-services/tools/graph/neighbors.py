import json
from tools.http_tool import BackendTool


class GraphNeighborsTool(BackendTool):
    def get_name(self) -> str:
        return "graph_neighbors"

    def get_description(self) -> str:
        return "Get direct neighbors of a node in the graph, optionally filtered by edge type."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "node_id": {"type": "string", "description": "Node ID to get neighbors for"},
                "edge_type": {"type": "string", "description": "Optional: filter by edge type (e.g., 'accomplice', 'family')"},
            },
            "required": ["node_id"],
        }

    async def execute(self, node_id: str = "", edge_type: str = None, **kwargs) -> str:
        url = f"/api/v1/graph/neighbors/{node_id}"
        if edge_type:
            url += f"?edge_type={edge_type}"
        result = await self._get(url)
        return json.dumps(result, default=str)
