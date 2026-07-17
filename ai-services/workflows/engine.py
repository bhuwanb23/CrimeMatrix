from typing import Dict, Any, List, Optional
from workflows.step import WorkflowStep
from workflows.state import WorkflowState
from workflows.registry import workflow_registry
import time
import structlog

logger = structlog.get_logger()


class WorkflowEngine:
    def __init__(self):
        self.registry = workflow_registry

    async def run(self, workflow_name: str, inputs: Dict = None) -> Dict:
        wf_def = self.registry.get(workflow_name)
        if not wf_def:
            return {"error": f"Workflow '{workflow_name}' not found"}

        state = WorkflowState(inputs or {})
        steps = wf_def.get("steps", [])
        executed = set()
        step_results = []
        total_start = time.time()

        for step_def in steps:
            step = WorkflowStep(
                name=step_def["name"],
                func=step_def["func"],
                description=step_def.get("description", ""),
                depends_on=step_def.get("depends_on", []),
            )

            for dep in step.depends_on:
                if dep not in executed:
                    logger.warning("workflow_step_dep_not_met", step=step.name, dep=dep)

            start = time.time()
            step.status = "running"
            try:
                result = await step.func(state)
                step.result = result
                step.status = "completed"
                state.set_step_result(step.name, result)
                executed.add(step.name)
            except Exception as e:
                step.status = "failed"
                step.error = str(e)
                logger.error("workflow_step_failed", step=step.name, error=str(e))

            step.duration_ms = round((time.time() - start) * 1000)
            step_results.append(step.to_dict())

        total_ms = round((time.time() - total_start) * 1000)
        failed = sum(1 for s in step_results if s["status"] == "failed")

        return {
            "workflow": workflow_name,
            "status": "completed" if failed == 0 else "partial" if failed < len(steps) else "failed",
            "steps": step_results,
            "total_steps": len(steps),
            "completed": len(executed),
            "failed": failed,
            "total_duration_ms": total_ms,
            "result": state.get_all(),
        }

    def list_workflows(self) -> list:
        return self.registry.list_all()

    def get_workflow(self, name: str) -> Optional[dict]:
        wf = self.registry.get(name)
        if wf:
            return {"name": name, "description": wf.get("description", ""), "steps": [s["name"] for s in wf.get("steps", [])]}
        return None
