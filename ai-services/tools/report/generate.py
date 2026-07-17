import json
from tools.http_tool import BackendTool


class ReportGenerateTool(BackendTool):
    def get_name(self) -> str:
        return "report_generate"

    def get_description(self) -> str:
        return "Generate a PDF report for a crime investigation."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "crime_id": {"type": "integer", "description": "Crime ID to generate report for"},
                "report_type": {"type": "string", "description": "Report type: 'investigation', 'summary', 'timeline', or 'evidence'", "default": "investigation"},
            },
            "required": ["crime_id"],
        }

    async def execute(self, crime_id: int = 0, report_type: str = "investigation", **kwargs) -> str:
        result = await self._post(f"/api/v1/reports/generate/{report_type}", {"crime_id": crime_id})
        return json.dumps(result, default=str)
