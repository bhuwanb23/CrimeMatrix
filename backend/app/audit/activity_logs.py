import uuid
from datetime import datetime
from typing import List
import structlog

logger = structlog.get_logger()


class ActivityLogStore:
    def __init__(self):
        self._logs: List[dict] = []

    def log(self, user_id: str, action: str, entity_type: str, entity_id: str = None,
            details: dict = None, ip_address: str = None) -> dict:
        entry = {
            "id": uuid.uuid4().hex[:12],
            "user_id": user_id,
            "action": action,
            "entity_type": entity_type,
            "entity_id": str(entity_id) if entity_id else None,
            "details": details or {},
            "ip_address": ip_address,
            "created_at": datetime.now().isoformat(),
        }
        self._logs.append(entry)
        if len(self._logs) > 10000:
            self._logs = self._logs[-10000:]
        return entry

    def list_logs(self, limit: int = 100, offset: int = 0, user_id: str = None,
                  action: str = None, entity_type: str = None) -> List[dict]:
        logs = self._logs
        if user_id:
            logs = [l for l in logs if l["user_id"] == user_id]
        if action:
            logs = [l for l in logs if l["action"] == action]
        if entity_type:
            logs = [l for l in logs if l["entity_type"] == entity_type]
        return list(reversed(logs))[offset:offset + limit]
