from tools.base import Tool
import httpx
import structlog

logger = structlog.get_logger()
BACKEND_URL = "http://localhost:8001"


class EvaluationReportTool(Tool):
    def get_name(self) -> str:
        return "evaluation_report"

    def get_description(self) -> str:
        return (
            "Generate or retrieve AI model evaluation reports. Provides accuracy, "
            "precision, recall, F1 scores, drift indicators, and feedback summaries. "
            "Use when an officer asks about AI performance or model quality."
        )

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["stats", "run", "results", "drift"], "default": "stats"},
            },
        }

    async def execute(self, action: str = "stats", **kwargs) -> str:
        try:
            async with httpx.AsyncClient() as client:
                if action == "run":
                    resp = await client.post(f"{self.backend_url}/api/v1/evaluation/run", json={}, timeout=30)
                elif action == "results":
                    resp = await client.get(f"{self.backend_url}/api/v1/evaluation/results", timeout=15)
                elif action == "drift":
                    resp = await client.get(f"{self.backend_url}/api/v1/evaluation/drift", timeout=15)
                else:
                    resp = await client.get(f"{self.backend_url}/api/v1/evaluation/stats", timeout=15)

                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    if action == "run":
                        return (
                            f"**Evaluation Complete:**\n"
                            f"- Accuracy: {data.get('accuracy', 0)}%\n"
                            f"- Precision: {data.get('precision', 0)}%\n"
                            f"- Recall: {data.get('recall', 0)}%\n"
                            f"- F1 Score: {data.get('f1_score', 0)}%\n"
                            f"- Sample size: {data.get('sample_size', 0)}"
                        )
                    elif action == "results":
                        items = data.get("items", [])
                        if not items:
                            return "No evaluation results yet."
                        lines = ["## Evaluation Results\n"]
                        for r in items[:5]:
                            lines.append(f"- **{r.get('model_name', 'unknown')}** ({r.get('evaluation_type', '')}): Acc={r.get('accuracy', 0)}%, F1={r.get('f1_score', 0)}%")
                        return "\n".join(lines)
                    elif action == "drift":
                        return f"**Drift Analysis:**\n- Drift: {data.get('drift', 0)}\n- Status: {data.get('status', 'unknown')}\n- Recent avg: {data.get('recent_avg', 0)}%\n- Older avg: {data.get('older_avg', 0)}%"
                    else:
                        return (
                            f"**Model Evaluation Stats:**\n"
                            f"- Total metrics: {data.get('total_metrics', 0)}\n"
                            f"- Total feedback: {data.get('total_feedback', 0)}\n"
                            f"- Total evaluations: {data.get('total_evaluations', 0)}\n"
                            f"- Avg rating: {data.get('avg_rating', 0)}/5"
                        )
                return f"Error: HTTP {resp.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
