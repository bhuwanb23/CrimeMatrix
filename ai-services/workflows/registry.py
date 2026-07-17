from typing import Dict, Optional
import structlog

logger = structlog.get_logger()


class WorkflowRegistry:
    def __init__(self):
        self._workflows: Dict[str, dict] = {}

    def register(self, name: str, workflow: dict):
        self._workflows[name] = workflow
        logger.info("workflow_registered", name=name)

    def get(self, name: str) -> Optional[dict]:
        return self._workflows.get(name)

    def list_all(self) -> list:
        return [
            {"name": k, "description": v.get("description", ""), "steps": len(v.get("steps", []))}
            for k, v in self._workflows.items()
        ]

    def get_step_names(self, name: str) -> list:
        wf = self._workflows.get(name, {})
        return [s["name"] for s in wf.get("steps", [])]


workflow_registry = WorkflowRegistry()
