from tools.base import Tool
import httpx
import structlog

logger = structlog.get_logger()
BACKEND_URL = "http://localhost:8001"


class EarlyWarningCheckTool(Tool):
    def get_name(self) -> str:
        return "early_warning_check"

    def get_description(self) -> str:
        return (
            "Check for early warning alerts — crime spikes, emerging hotspots, "
            "serial offenses, and cross-district escalation. "
            "Use when an officer asks about alerts or potential risks."
        )

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["list", "detect", "stats"], "default": "list"},
                "severity": {"type": "string", "enum": ["critical", "high", "medium", "low"], "description": "Filter by severity"},
            },
        }

    async def execute(self, action: str = "list", severity: str = None, **kwargs) -> str:
        try:
            async with httpx.AsyncClient() as client:
                if action == "detect":
                    resp = await client.post(f"{self.backend_url}/api/v1/early-warning/detect", json={}, timeout=30)
                elif action == "stats":
                    resp = await client.get(f"{self.backend_url}/api/v1/early-warning/stats", timeout=15)
                else:
                    params = {}
                    if severity:
                        params["severity"] = severity
                    resp = await client.get(f"{self.backend_url}/api/v1/early-warning/alerts", params=params, timeout=15)

                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    if action == "detect":
                        return f"**Detection Complete:**\n- Spike alerts: {data.get('spike_alerts', 0)}\n- Hotspot alerts: {data.get('hotspot_alerts', 0)}\n- Serial alerts: {data.get('serial_alerts', 0)}\n- Escalation alerts: {data.get('escalation_alerts', 0)}\n- Total created: {data.get('alerts_created', 0)}"
                    elif action == "stats":
                        return f"**Early Warning Stats:**\n- Total: {data.get('total', 0)}\n- Active: {data.get('active', 0)}\n- Critical: {data.get('critical', 0)}\n- High: {data.get('high', 0)}"
                    else:
                        items = data.get("items", [])
                        if not items:
                            return "No active alerts."
                        lines = ["## Active Alerts\n"]
                        for a in items[:10]:
                            lines.append(f"- **{a.get('title', 'Unknown')}** ({a.get('severity', 'unknown')}) — Confidence: {a.get('confidence', 0)}%")
                        return "\n".join(lines)
                return f"Error: HTTP {resp.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
