import json
from tools.base import Tool


class WorkflowRunTool(Tool):
    def __init__(self):
        self._engine = None

    def _get_engine(self):
        if self._engine is None:
            from workflows.engine import WorkflowEngine
            self._engine = WorkflowEngine()
        return self._engine

    def get_name(self) -> str:
        return "workflow_run"

    def get_description(self) -> str:
        return "Run a pre-built investigation workflow: investigation, case_analysis, suspect_profile, or crime_briefing."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "workflow": {"type": "string", "description": "Workflow name: 'investigation', 'case_analysis', 'suspect_profile', 'crime_briefing'"},
                "inputs": {"type": "object", "description": "Input parameters for the workflow"},
            },
            "required": ["workflow"],
        }

    async def execute(self, workflow: str = "", inputs: dict = None, **kwargs) -> str:
        engine = self._get_engine()
        result = await engine.run(workflow, inputs or {})
        return json.dumps(result, default=str)
