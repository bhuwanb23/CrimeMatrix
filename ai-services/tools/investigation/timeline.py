import json
from tools.http_tool import BackendTool


class InvestigationTimelineTool(BackendTool):
    def get_name(self) -> str:
        return "investigation_timeline"

    def get_description(self) -> str:
        return "Get timeline events for an investigation."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "investigation_id": {"type": "integer", "description": "Investigation ID to get timeline for"},
            },
            "required": ["investigation_id"],
        }

    async def execute(self, investigation_id: int = 0, **kwargs) -> str:
        result = await self._get(f"/api/v1/timeline/?investigation_id={investigation_id}")
        return json.dumps(result, default=str)
