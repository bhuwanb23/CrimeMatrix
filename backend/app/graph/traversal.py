from typing import List, Dict
from app.graph.network import GraphManager
import networkx as nx
import structlog

logger = structlog.get_logger()


class TraversalEngine:
    def __init__(self, graph: GraphManager):
        self.graph = graph

    def bfs(self, start: str, max_depth: int = 5) -> List[Dict]:
        try:
            visited = set()
            queue = [(start, 0)]
            result = []

            while queue:
                node, depth = queue.pop(0)
                if node in visited or depth > max_depth:
                    continue
                visited.add(node)

                node_data = dict(self.graph.graph.nodes.get(node, {}))
                node_data["id"] = node
                node_data["depth"] = depth
                result.append(node_data)

                for neighbor in self.graph.graph.neighbors(node):
                    if neighbor not in visited:
                        queue.append((neighbor, depth + 1))

            return result
        except Exception as e:
            logger.error("bfs_error", error=str(e))
            return []

    def dfs(self, start: str, max_depth: int = 5) -> List[Dict]:
        try:
            visited = set()
            result = []

            def dfs_recursive(node, depth):
                if node in visited or depth > max_depth:
                    return
                visited.add(node)
                node_data = dict(self.graph.graph.nodes.get(node, {}))
                node_data["id"] = node
                node_data["depth"] = depth
                result.append(node_data)
                for neighbor in self.graph.graph.neighbors(node):
                    dfs_recursive(neighbor, depth + 1)

            dfs_recursive(start, 0)
            return result
        except Exception as e:
            logger.error("dfs_error", error=str(e))
            return []

    def find_all_paths(self, source: str, target: str, max_length: int = 5) -> List[List[str]]:
        try:
            return list(nx.all_simple_paths(self.graph.graph, source, target, cutoff=max_length))
        except nx.NetworkXError:
            return []
