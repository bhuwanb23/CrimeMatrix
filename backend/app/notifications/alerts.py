import uuid
from datetime import datetime
from typing import Dict, List, Optional
import structlog

logger = structlog.get_logger()


class AlertQueue:
    def __init__(self):
        self._alerts: Dict[str, dict] = {}
        self._queue: List[str] = []

    def submit(self, alert_type: str, title: str, message: str, priority: str = "medium", data: dict = None) -> dict:
        alert_id = uuid.uuid4().hex[:12]
        alert = {
            "id": alert_id,
            "type": alert_type,
            "title": title,
            "message": message,
            "priority": priority,
            "data": data or {},
            "status": "queued",
            "created_at": datetime.now().isoformat(),
            "processed_at": None,
        }
        self._alerts[alert_id] = alert
        self._queue.append(alert_id)
        logger.info("alert_queued", alert_id=alert_id, type=alert_type, priority=priority)
        return alert

    def get_alert(self, alert_id: str) -> Optional[dict]:
        return self._alerts.get(alert_id)

    def list_alerts(self, status: str = None) -> List[dict]:
        alerts = list(self._alerts.values())
        if status:
            alerts = [a for a in alerts if a["status"] == status]
        alerts.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return alerts

    def process_next(self) -> Optional[dict]:
        while self._queue:
            alert_id = self._queue.pop(0)
            alert = self._alerts.get(alert_id)
            if alert and alert["status"] == "queued":
                alert["status"] = "processed"
                alert["processed_at"] = datetime.now().isoformat()
                return alert
        return None

    def get_queue_size(self) -> int:
        return len(self._queue)

    def get_stats(self) -> dict:
        total = len(self._alerts)
        queued = sum(1 for a in self._alerts.values() if a["status"] == "queued")
        processed = sum(1 for a in self._alerts.values() if a["status"] == "processed")
        return {"total": total, "queued": queued, "processed": processed}
