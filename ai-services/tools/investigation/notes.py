import json
from tools.http_tool import BackendTool


class InvestigationNotesTool(BackendTool):
    def get_name(self) -> str:
        return "investigation_notes"

    def get_description(self) -> str:
        return "List or create investigation notes for a case."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "'list' or 'create'", "default": "list"},
                "content": {"type": "string", "description": "Note content (for create)"},
                "investigation_id": {"type": "integer", "description": "Investigation ID (for create)"},
            },
        }

    async def execute(self, action: str = "list", content: str = None,
                      investigation_id: int = None, **kwargs) -> str:
        if action == "create" and content and investigation_id:
            result = await self._post("/api/v1/notes/", {
                "content": content,
                "investigation_id": investigation_id,
            })
        else:
            result = await self._get("/api/v1/notes/")
        return json.dumps(result, default=str)
