from fastapi import APIRouter, Query
from app.graph.network import GraphManager
from app.graph.nodes import NodeManager
from app.graph.relationships import RelationshipManager
from app.graph.traversal import TraversalEngine
from app.graph.shortest_path import PathFinder
from app.graph.neighbors import NeighborFinder
from app.graph.components import ComponentAnalyzer
from app.graph.timeline import TimelineAnalyzer
from app.core.response import success_response
from pydantic import BaseModel
from typing import Optional, Dict, Any
import networkx as nx

router = APIRouter()

# Shared graph instance
graph = GraphManager()
node_mgr = NodeManager(graph)
rel_mgr = RelationshipManager(graph)
traversal = TraversalEngine(graph)
path_finder = PathFinder(graph)
neighbor_finder = NeighborFinder(graph)
component_analyzer = ComponentAnalyzer(graph)
timeline_analyzer = TimelineAnalyzer(graph)


class NodeCreate(BaseModel):
    node_id: str
    node_type: str
    name: Optional[str] = None
    attrs: Optional[Dict[str, Any]] = None


class EdgeCreate(BaseModel):
    source: str
    target: str
    edge_type: str
    attrs: Optional[Dict[str, Any]] = None


# Nodes
@router.get("/nodes")
async def list_nodes():
    return success_response(data=node_mgr.get_all_nodes())


@router.get("/nodes/{node_id}")
async def get_node(node_id: str):
    node = node_mgr.get_node(node_id)
    if not node:
        return success_response(message="Node not found")
    return success_response(data=node)


@router.post("/nodes")
async def create_node(data: NodeCreate):
    result = node_mgr.add_node(data.node_id, data.node_type, **(data.attrs or {}))
    return success_response(data=result, message="Node created")


@router.put("/nodes/{node_id}")
async def update_node(node_id: str, data: NodeCreate):
    result = node_mgr.update_node(node_id, **(data.attrs or {}))
    if not result:
        return success_response(message="Node not found")
    return success_response(data=result, message="Node updated")


@router.delete("/nodes/{node_id}")
async def delete_node(node_id: str):
    deleted = node_mgr.delete_node(node_id)
    return success_response(message="Node deleted" if deleted else "Node not found")


@router.get("/nodes/search/{query}")
async def search_nodes(query: str):
    results = node_mgr.search_nodes(query)
    return success_response(data=results)


# Edges
@router.get("/edges")
async def list_edges():
    return success_response(data=rel_mgr.get_edges())


@router.post("/edges")
async def create_edge(data: EdgeCreate):
    result = rel_mgr.add_edge(data.source, data.target, data.edge_type, **(data.attrs or {}))
    return success_response(data=result, message="Edge created")


@router.delete("/edges/{source}/{target}")
async def delete_edge(source: str, target: str):
    deleted = rel_mgr.delete_edge(source, target)
    return success_response(message="Edge deleted" if deleted else "Edge not found")


@router.get("/edges/{node_id}")
async def get_node_edges(node_id: str):
    edges = rel_mgr.get_node_edges(node_id)
    return success_response(data=edges)


# Traversal
@router.get("/traverse/{node_id}")
async def traverse(node_id: str, method: str = "bfs", max_depth: int = 5):
    if method == "dfs":
        result = traversal.dfs(node_id, max_depth)
    else:
        result = traversal.bfs(node_id, max_depth)
    return success_response(data=result)


@router.get("/paths/{source}/{target}")
async def find_paths(source: str, target: str, max_length: int = 5):
    paths = traversal.find_all_paths(source, target, max_length)
    return success_response(data=paths)


# Shortest Path
@router.get("/shortest/{source}/{target}")
async def shortest_path(source: str, target: str):
    path = path_finder.shortest_path(source, target)
    if not path:
        return success_response(message="No path found")
    details = path_finder.get_path_details(path)
    return success_response(data={"path": path, "details": details, "length": len(path) - 1})


# Neighbors
@router.get("/neighbors/{node_id}")
async def get_neighbors(node_id: str, edge_type: str = None):
    if edge_type:
        neighbors = neighbor_finder.get_neighbors_by_type(node_id, edge_type)
    else:
        neighbors = neighbor_finder.get_neighbors(node_id)
    return success_response(data=neighbors)


# Connected Components
@router.get("/components")
async def get_components():
    components = component_analyzer.get_connected_components()
    stats = component_analyzer.get_component_stats()
    return success_response(data={"components": components, "stats": stats})


@router.get("/components/largest")
async def get_largest_component():
    component = component_analyzer.get_largest_component()
    return success_response(data=component)


# Timeline
@router.get("/timeline")
async def get_timeline():
    timeline = timeline_analyzer.get_activity_timeline()
    return success_response(data=timeline)


@router.get("/timeline/{node_id}")
async def get_node_timeline(node_id: str):
    timeline = timeline_analyzer.get_node_timeline(node_id)
    return success_response(data=timeline)


# Graph Stats
@router.get("/stats")
async def get_graph_stats():
    stats = component_analyzer.get_component_stats()
    stats["total_nodes"] = graph.graph.number_of_nodes()
    stats["total_edges"] = graph.graph.number_of_edges()
    stats["density"] = round(nx.density(graph.graph), 4) if graph.graph.number_of_nodes() > 1 else 0
    return success_response(data=stats)


# Graph Persistence (SQLite ↔ NetworkX)
from app.db.session import get_db
from app.graph.loader import GraphLoader
from app.graph.sync import GraphSync


@router.post("/load")
async def load_graph():
    db = None
    async for session in get_db():
        db = session
        break
    if not db:
        return success_response(message="No DB session")
    loader = GraphLoader(db)
    stats = await loader.load()
    graph.graph = loader.graph
    node_mgr.graph = graph.graph
    rel_mgr.graph = graph.graph
    traversal.graph = graph.graph
    path_finder.graph = graph.graph
    neighbor_finder.graph = graph.graph
    component_analyzer.graph = graph.graph
    timeline_analyzer.graph = graph.graph
    return success_response(data=stats, message="Graph loaded from SQLite")


@router.post("/save")
async def save_graph():
    db = None
    async for session in get_db():
        db = session
        break
    if not db:
        return success_response(message="No DB session")
    loader = GraphLoader(db)
    loader.graph = graph.graph
    stats = await loader.save()
    return success_response(data=stats, message="Graph saved to SQLite")


class NodeCreateFull(BaseModel):
    node_id: str
    node_type: str = "unknown"
    properties: Optional[dict] = None
    confidence: float = 1.0


class EdgeCreateFull(BaseModel):
    source: str
    target: str
    relation: str = ""
    properties: Optional[dict] = None
    weight: float = 1.0


@router.post("/nodes")
async def create_node_full(data: NodeCreateFull):
    props = data.properties or {}
    graph.graph.add_node(data.node_id, type=data.node_type, confidence=data.confidence, **props)
    return success_response(data={"node_id": data.node_id, "confidence": data.confidence})


@router.post("/edges")
async def create_edge_full(data: EdgeCreateFull):
    props = data.properties or {}
    graph.graph.add_edge(data.source, data.target, relation=data.relation, weight=data.weight, **props)
    return success_response(data={"source": data.source, "target": data.target, "weight": data.weight})


@router.post("/save-all")
async def save_all_nodes_edges(data: dict):
    db = None
    async for session in get_db():
        db = session
        break
    if not db:
        return success_response(message="No DB session")
    loader = GraphLoader(db)
    loader.graph = graph.graph
    stats = await loader.save()
    return success_response(data=stats)


@router.post("/build-from-crimes")
async def build_graph_from_crimes():
    from sqlalchemy import select
    from app.models.suspect import Suspect
    from app.models.criminal import Criminal
    from app.models.victim import Victim
    from app.models.witness import Witness
    from app.models.vehicle import Vehicle
    from app.models.phone import Phone
    from app.models.crime import Crime
    from app.models.evidence import Evidence

    db = None
    async for session in get_db():
        db = session
        break
    if not db:
        return success_response(message="No DB session")

    nodes_created = 0
    edges_created = 0

    # Add suspects
    result = await db.execute(select(Suspect))
    for s in result.scalars().all():
        node_id = f"S_{s.id}"
        if node_id not in graph.graph:
            graph.graph.add_node(node_id, node_type="suspect", label=s.name, risk=s.risk_score or 0, district=s.district or "", status=s.status or "")
            nodes_created += 1

    # Add criminals
    result = await db.execute(select(Criminal))
    for c in result.scalars().all():
        node_id = f"CR_{c.id}"
        if node_id not in graph.graph:
            graph.graph.add_node(node_id, node_type="criminal", label=c.alias or f"Criminal #{c.id}", risk=c.risk_score or 0, status=c.status or "")
            nodes_created += 1
        if c.person_id:
            person_node = f"S_{c.person_id}"
            if person_node in graph.graph and not graph.graph.has_edge(person_node, node_id):
                graph.graph.add_edge(person_node, node_id, relation="is_criminal", weight=1.0)
                edges_created += 1

    # Add vehicles
    result = await db.execute(select(Vehicle))
    for v in result.scalars().all():
        node_id = f"V_{v.id}"
        if node_id not in graph.graph:
            graph.graph.add_node(node_id, node_type="vehicle", label=v.registration_number or f"Vehicle #{v.id}", make=v.make or "", model=v.model or "", color=v.color or "")
            nodes_created += 1

    # Add phones
    result = await db.execute(select(Phone))
    for p in result.scalars().all():
        node_id = f"P_{p.id}"
        if node_id not in graph.graph:
            graph.graph.add_node(node_id, node_type="phone", label=p.number or f"Phone #{p.id}", carrier=p.carrier or "")
            nodes_created += 1

    # Add evidence
    result = await db.execute(select(Evidence))
    for e in result.scalars().all():
        node_id = f"E_{e.id}"
        if node_id not in graph.graph:
            graph.graph.add_node(node_id, node_type="evidence", label=f"{e.evidence_type} #{e.id}", evidence_type=e.evidence_type or "", status=e.status or "")
            nodes_created += 1

    stats = {"nodes_created": nodes_created, "edges_created": edges_created, "total_nodes": graph.graph.number_of_nodes(), "total_edges": graph.graph.number_of_edges()}
    return success_response(data=stats, message="Graph built from crime data")
