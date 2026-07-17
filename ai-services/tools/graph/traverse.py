import json
from tools.http_tool import BackendTool


class GraphTraverseTool(BackendTool):
    def get_name(self) -> str:
        return "graph_traverse"

    def get_description(self) -> str:
        return "Traverse a graph from a starting node using BFS or DFS. Returns connected nodes."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "node_id": {"type": "string", "description": "Starting node ID (e.g., 'suspect_001')"},
                "method": {"type": "string", "description": "Traversal method: 'bfs' or 'dfs'", "default": "bfs"},
                "max_depth": {"type": "integer", "description": "Maximum depth", "default": 3},
            },
            "required": ["node_id"],
        }

    async def execute(self, node_id: str = "", method: str = "bfs", max_depth: int = 3, **kwargs) -> str:
        result = await self._get(f"/api/v1/graph/traverse/{node_id}?method={method}&max_depth={max_depth}")
        return json.dumps(result, default=str)
