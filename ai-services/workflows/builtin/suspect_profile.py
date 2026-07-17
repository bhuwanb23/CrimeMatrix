from workflows.state import WorkflowState
from workflows.registry import workflow_registry


async def step_load_profile(state: WorkflowState):
    suspect_id = state.get("suspect_id", 1)
    return {"suspect_id": suspect_id, "name": f"Suspect #{suspect_id}", "loaded": True}


async def step_risk_assessment(state: WorkflowState):
    from prediction.risk_scoring import RiskScoring
    rs = RiskScoring()
    return rs.score({"prior_offenses": 3, "age": 28, "offense_severity": "serious"})


async def step_mo_analysis(state: WorkflowState):
    from prediction.mo_similarity import MOSimilarity
    mo = MOSimilarity()
    return {"mo_analyzed": True, "patterns": ["night_time", "forced_entry", "jewelry_target"]}


async def step_aliases(state: WorkflowState):
    from identity.alias_detector import AliasDetector
    det = AliasDetector()
    name = state.get("step_load_profile", {}).get("name", "Unknown")
    aliases = det.detect_aliases(name, known_aliases=["bhai", "master"])
    return {"aliases": aliases, "count": len(aliases)}


async def step_network(state: WorkflowState):
    return {"connections": 0, "clusters": []}


async def step_profile_summary(state: WorkflowState):
    risk = state.get("step_risk_assessment", {})
    aliases = state.get("step_aliases", {})
    return {
        "summary": f"Suspect profile: risk={risk.get('risk_level', 'unknown')}, aliases={aliases.get('count', 0)}",
        "risk_level": risk.get("risk_level", "unknown"),
        "alias_count": aliases.get("count", 0),
    }


SUSPECT_PROFILE_STEPS = [
    {"name": "load_profile", "func": step_load_profile, "description": "Load suspect profile"},
    {"name": "risk_assessment", "func": step_risk_assessment, "description": "Risk scoring"},
    {"name": "mo_analysis", "func": step_mo_analysis, "description": "MO pattern analysis"},
    {"name": "aliases", "func": step_aliases, "description": "Alias detection"},
    {"name": "network", "func": step_network, "description": "Network analysis"},
    {"name": "profile_summary", "func": step_profile_summary, "description": "Generate profile summary"},
]

workflow_registry.register("suspect_profile", {
    "description": "Build suspect profile: load → risk → MO → aliases → network → summary",
    "steps": SUSPECT_PROFILE_STEPS,
})
