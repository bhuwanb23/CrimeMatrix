from workflows.state import WorkflowState
from workflows.registry import workflow_registry


async def step_load_data(state: WorkflowState):
    return {"crime_data": [], "loaded": True}


async def step_statistics(state: WorkflowState):
    return {"total_crimes": 0, "active_cases": 0, "resolution_rate": 0}


async def step_trends(state: WorkflowState):
    return {"trend": "stable", "slope": 0}


async def step_hotspots(state: WorkflowState):
    return {"hotspots": [], "top_location": "unknown"}


async def step_summary(state: WorkflowState):
    stats = state.get("step_statistics", {})
    trends = state.get("step_trends", {})
    hotspots = state.get("step_hotspots", {})
    return {
        "briefing": f"Crime briefing: {stats.get('total_crimes', 0)} crimes, trend: {trends.get('trend', 'unknown')}",
        "statistics": stats,
        "trends": trends,
        "hotspots": hotspots,
    }


CRIME_BRIEFING_STEPS = [
    {"name": "load_data", "func": step_load_data, "description": "Load crime data"},
    {"name": "statistics", "func": step_statistics, "description": "Compute statistics"},
    {"name": "trends", "func": step_trends, "description": "Analyze trends"},
    {"name": "hotspots", "func": step_hotspots, "description": "Identify hotspots"},
    {"name": "summary", "func": step_summary, "description": "Generate briefing summary"},
]

workflow_registry.register("crime_briefing", {
    "description": "Generate crime briefing: data → stats → trends → hotspots → summary",
    "steps": CRIME_BRIEFING_STEPS,
})
