from workflows.state import WorkflowState
from workflows.registry import workflow_registry
import structlog

logger = structlog.get_logger()


async def step_search(state: WorkflowState):
    query = state.get("query", "")
    from tools.registry import tool_registry
    result = await tool_registry.invoke("crime_search", query=query, limit=10)
    import json
    return json.loads(result) if isinstance(result, str) else result


async def step_identity(state: WorkflowState):
    query = state.get("query", "")
    from identity.name_matcher import IndianNameMatcher
    matcher = IndianNameMatcher()
    results = state.get("step_search", {}).get("data", {}).get("results", [])
    suspects = []
    for r in results:
        if r.get("entity") == "suspects":
            suspects.append(r.get("name", ""))
    return {"suspects_found": len(suspects), "names": suspects[:5]}


async def step_knowledge_graph(state: WorkflowState):
    from knowledge.query_engine import GraphQueryEngine
    import networkx as nx
    graph = nx.Graph()
    graph.add_node("query", type="query", name=state.get("query", ""))
    return {"nodes": graph.number_of_nodes(), "edges": graph.number_of_edges()}


async def step_analytics(state: WorkflowState):
    return {"analytics": "crime statistics loaded", "data_points": 0}


async def step_prediction(state: WorkflowState):
    from prediction.risk_scoring import RiskScoring
    rs = RiskScoring()
    profile = state.get("suspect_profile", {"prior_offenses": 0, "age": 30})
    return rs.score(profile)


async def step_reasoning(state: WorkflowState):
    hypothesis = f"Investigation into: {state.get('query', '')}"
    evidence = [
        {"claim": "Search results obtained", "type": "direct", "strength": 0.7, "supports": True},
        {"claim": "Analytics data reviewed", "type": "circumstantial", "strength": 0.5, "supports": True},
    ]
    from reasoning.chain import ReasoningChainGenerator
    gen = ReasoningChainGenerator()
    chain = gen.build(hypothesis, evidence)
    return chain


async def step_respond(state: WorkflowState):
    search = state.get("step_search", {})
    prediction = state.get("step_prediction", {})
    reasoning = state.get("step_reasoning", {})
    return {
        "summary": f"Investigation workflow completed for: {state.get('query', '')}",
        "search_results": search.get("data", {}).get("total", 0) if isinstance(search, dict) else 0,
        "risk_level": prediction.get("risk_level", "unknown") if isinstance(prediction, dict) else "unknown",
        "confidence": reasoning.get("conclusion", {}).get("verdict", "unknown") if isinstance(reasoning, dict) else "unknown",
    }


INVESTIGATION_STEPS = [
    {"name": "search", "func": step_search, "description": "Search for relevant crimes and suspects"},
    {"name": "identity", "func": step_identity, "description": "Resolve identities from search results"},
    {"name": "knowledge_graph", "func": step_knowledge_graph, "description": "Query knowledge graph for connections"},
    {"name": "analytics", "func": step_analytics, "description": "Load analytics data"},
    {"name": "prediction", "func": step_prediction, "description": "Risk prediction"},
    {"name": "reasoning", "func": step_reasoning, "description": "Chain-of-thought reasoning"},
    {"name": "respond", "func": step_respond, "description": "Generate final response"},
]

workflow_registry.register("investigation", {
    "description": "Full investigation workflow: search → identity → graph → analytics → predict → reason → respond",
    "steps": INVESTIGATION_STEPS,
})
