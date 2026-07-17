import json
from tools.base import Tool


class KnowledgeGraphTool(Tool):
    def __init__(self):
        self._builder = None

    def _get_builder(self):
        if self._builder is None:
            from knowledge.graph_builder import GraphBuilder
            self._builder = GraphBuilder()
        return self._builder

    def get_name(self) -> str:
        return "knowledge_graph"

    def get_description(self) -> str:
        return "Query the criminal knowledge graph — find connections, analyze networks, discover relationships, generate timelines."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query_type": {"type": "string", "description": "Query type: 'build', 'crimes_linked', 'network_clusters', 'shortest_path', 'centrality', 'timeline'"},
                "node_id": {"type": "string", "description": "Node ID (e.g., 'person_1', 'crime_2')"},
                "node_id_2": {"type": "string", "description": "Second node for path/strength queries"},
            },
            "required": ["query_type"],
        }

    async def execute(self, query_type: str = "", node_id: str = None,
                      node_id_2: str = None, **kwargs) -> str:
        from knowledge.query_engine import GraphQueryEngine
        from knowledge.criminal_network import CriminalNetwork
        from knowledge.link_analysis import LinkAnalysis
        from knowledge.timeline_gen import TimelineGenerator

        builder = self._get_builder()
        if query_type == "build":
            stats = await builder.build()
            return json.dumps(stats)

        qe = GraphQueryEngine(builder.graph)
        cn = CriminalNetwork(builder.graph)
        la = LinkAnalysis(builder.graph)
        tg = TimelineGenerator(builder.graph)

        if query_type == "crimes_linked" and node_id:
            result = qe.crimes_linked_to(node_id)
        elif query_type == "network_clusters":
            result = cn.find_clusters()
        elif query_type == "risk" and node_id:
            result = cn.network_risk_score(node_id)
        elif query_type == "shortest_path" and node_id and node_id_2:
            result = la.shortest_path(node_id, node_id_2)
        elif query_type == "centrality":
            result = la.centrality()
        elif query_type == "timeline":
            result = tg.generate()
        else:
            result = {"error": f"Unknown query: {query_type}"}

        return json.dumps(result, default=str)
