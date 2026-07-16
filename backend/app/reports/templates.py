from typing import Dict, Any, List
import structlog

logger = structlog.get_logger()

TEMPLATES = {
    "investigation": {
        "id": "investigation",
        "name": "Investigation Report",
        "description": "Full investigation report with case details, timeline, evidence, and notes",
        "sections": ["header", "case_summary", "timeline", "evidence", "notes", "footer"],
    },
    "timeline": {
        "id": "timeline",
        "name": "Timeline Report",
        "description": "Chronological timeline of events and activities",
        "sections": ["header", "timeline", "footer"],
    },
    "evidence": {
        "id": "evidence",
        "name": "Evidence Report",
        "description": "Detailed evidence catalog with chain of custody",
        "sections": ["header", "evidence_list", "evidence_details", "footer"],
    },
    "summary": {
        "id": "summary",
        "name": "Case Summary Report",
        "description": "Executive summary of case status and key findings",
        "sections": ["header", "summary", "key_metrics", "footer"],
    },
}


class TemplateEngine:
    def list_templates(self) -> List[Dict]:
        return list(TEMPLATES.values())

    def get_template(self, template_id: str) -> Dict:
        return TEMPLATES.get(template_id, {"error": f"Template '{template_id}' not found"})
