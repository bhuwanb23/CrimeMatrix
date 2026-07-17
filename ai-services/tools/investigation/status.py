import json
from tools.http_tool import BackendTool


class CaseStatusTool(BackendTool):
    def get_name(self) -> str:
        return "case_status"

    def get_description(self) -> str:
        return "Update the status of a case (e.g., open, active, closed)."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "investigation_id": {"type": "integer", "description": "Investigation ID"},
                "new_status": {"type": "string", "description": "New status (e.g., 'active', 'closed')"},
                "notes": {"type": "string", "description": "Reason for status change"},
            },
            "required": ["investigation_id", "new_status"],
        }

    async def execute(self, investigation_id: int = 0, new_status: str = "",
                      notes: str = "", **kwargs) -> str:
        result = await self._post("/api/v1/case-status/", {
            "investigation_id": investigation_id,
            "new_status": new_status,
            "notes": notes,
        })
        return json.dumps(result, default=str)
