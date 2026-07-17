from workflows.state import WorkflowState
from workflows.registry import workflow_registry


async def step_load_case(state: WorkflowState):
    case_id = state.get("case_id", 1)
    return {"case_id": case_id, "loaded": True, "title": f"Case #{case_id}"}


async def step_embed(state: WorkflowState):
    case = state.get("step_load_case", {})
    from embeddings.service import EmbeddingService
    svc = EmbeddingService()
    vec = await svc.embed(case.get("title", ""), "fir", f"case_{case.get('case_id', 0)}")
    return {"embedding_dimension": len(vec), "embedded": True}


async def step_find_similar(state: WorkflowState):
    return {"similar_cases": [], "count": 0}


async def step_rank(state: WorkflowState):
    similar = state.get("step_find_similar", {}).get("similar_cases", [])
    return {"ranked": similar, "top_match": similar[0] if similar else None}


async def step_explain(state: WorkflowState):
    return {"explanation": f"Case analysis complete for case #{state.get('case_id', 'unknown')}"}


CASE_ANALYSIS_STEPS = [
    {"name": "load_case", "func": step_load_case, "description": "Load case data from backend"},
    {"name": "embed", "func": step_embed, "description": "Generate case embedding"},
    {"name": "find_similar", "func": step_find_similar, "description": "Find similar cases"},
    {"name": "rank", "func": step_rank, "description": "Rank similar cases"},
    {"name": "explain", "func": step_explain, "description": "Generate explanation"},
]

workflow_registry.register("case_analysis", {
    "description": "Analyze a case: load → embed → find similar → rank → explain",
    "steps": CASE_ANALYSIS_STEPS,
})
