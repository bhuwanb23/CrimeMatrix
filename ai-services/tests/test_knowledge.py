import pytest
import networkx as nx
from knowledge.graph_builder import GraphBuilder
from knowledge.query_engine import GraphQueryEngine
from knowledge.criminal_network import CriminalNetwork
from knowledge.relationship import RelationshipDiscovery
from knowledge.timeline_gen import TimelineGenerator
from knowledge.link_analysis import LinkAnalysis


def _make_graph():
    g = nx.Graph()
    g.add_node("person_1", type="person", name="Rajesh Kumar")
    g.add_node("person_2", type="person", name="Suresh Patel")
    g.add_node("person_3", type="person", name="John Doe")
    g.add_node("crime_1", type="crime", name="Theft at MG Road")
    g.add_node("crime_2", type="crime", name="Robbery Case")
    g.add_node("officer_1", type="officer", name="Inspector Singh")
    g.add_edge("person_1", "crime_1", relation="involved_in")
    g.add_edge("person_1", "crime_2", relation="involved_in")
    g.add_edge("person_2", "crime_2", relation="involved_in")
    g.add_edge("person_3", "crime_1", relation="witness")
    g.add_edge("officer_1", "crime_1", relation="investigating")
    return g


class TestGraphBuilder:
    def test_build_stats_empty(self):
        builder = GraphBuilder()
        stats = builder.get_stats()
        assert stats["nodes"] == 0

    def test_manual_edge(self):
        builder = GraphBuilder()
        builder.add_manual_edge("a", "b", "related")
        assert builder.graph.has_edge("a", "b")


class TestGraphQueryEngine:
    def setup_method(self):
        self.qe = GraphQueryEngine(_make_graph())

    def test_crimes_linked_to(self):
        results = self.qe.crimes_linked_to("person_1")
        assert len(results) == 2

    def test_suspects_in_crime(self):
        results = self.qe.suspects_in_crime("crime_1")
        assert len(results) >= 1

    def test_common_crimes(self):
        results = self.qe.common_crimes("person_1", "person_2")
        assert len(results) == 1

    def test_find_paths(self):
        paths = self.qe.find_paths("person_1", "officer_1")
        assert len(paths) > 0

    def test_search_nodes(self):
        results = self.qe.search_nodes("rajesh")
        assert len(results) == 1

    def test_subgraph(self):
        sg = self.qe.subgraph("person_1", depth=1)
        assert sg.number_of_nodes() > 0


class TestCriminalNetwork:
    def setup_method(self):
        self.cn = CriminalNetwork(_make_graph())

    def test_find_clusters(self):
        clusters = self.cn.find_clusters()
        assert len(clusters) > 0
        assert clusters[0]["size"] > 0

    def test_network_risk_score(self):
        risk = self.cn.network_risk_score("person_1")
        assert "risk" in risk
        assert risk["risk"] > 0

    def test_accomplice_network(self):
        net = self.cn.accomplice_network("person_1", depth=1)
        assert len(net["nodes"]) > 0
        assert len(net["edges"]) > 0

    def test_risk_nonexistent(self):
        risk = self.cn.network_risk_score("nonexistent")
        assert risk["risk"] == 0


class TestRelationshipDiscovery:
    def setup_method(self):
        self.rd = RelationshipDiscovery(_make_graph())

    def test_hidden_connections(self):
        paths = self.rd.find_hidden_connections("person_1", "officer_1")
        assert len(paths) > 0

    def test_shared_connections(self):
        shared = self.rd.shared_connections("person_1", "person_2")
        assert len(shared) >= 1

    def test_relationship_strength(self):
        strength = self.rd.relationship_strength("person_1", "person_2")
        assert strength["strength"] > 0

    def test_node_importance(self):
        importance = self.rd.node_importance("person_1")
        assert importance["importance"] > 0


class TestTimelineGenerator:
    def setup_method(self):
        g = _make_graph()
        g.nodes["crime_1"]["created_at"] = "2024-01-15"
        g.nodes["crime_2"]["created_at"] = "2024-02-20"
        g.edges["person_1", "crime_1"]["date"] = "2024-01-16"
        self.tg = TimelineGenerator(g)

    def test_generate(self):
        events = self.tg.generate()
        assert len(events) > 0

    def test_entity_timeline(self):
        events = self.tg.entity_timeline("person_1")
        assert len(events) > 0

    def test_activity_bursts(self):
        bursts = self.tg.activity_bursts()
        assert isinstance(bursts, list)


class TestLinkAnalysis:
    def setup_method(self):
        self.la = LinkAnalysis(_make_graph())

    def test_shortest_path(self):
        result = self.la.shortest_path("person_1", "officer_1")
        assert result["length"] > 0
        assert len(result["details"]) > 0

    def test_centrality(self):
        centrality = self.la.centrality()
        assert len(centrality) > 0
        assert "importance_score" in centrality[0]

    def test_communities(self):
        communities = self.la.communities()
        assert len(communities) > 0

    def test_bridges(self):
        bridges = self.la.bridges()
        assert isinstance(bridges, list)

    def test_isolated_nodes(self):
        g = _make_graph()
        g.add_node("isolated", type="person")
        la = LinkAnalysis(g)
        isolated = la.isolated_nodes()
        assert "isolated" in isolated

    def test_shortest_no_path(self):
        g = nx.Graph()
        g.add_node("a")
        g.add_node("b")
        la = LinkAnalysis(g)
        result = la.shortest_path("a", "b")
        assert result["length"] == -1
