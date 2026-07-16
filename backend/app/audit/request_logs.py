import uuid
from datetime import datetime
from typing import Dict, List, Optional
import structlog

logger = structlog.get_logger()


class RequestLogStore:
    def __init__(self):
        self._logs: List[dict] = []
        self._max_size = 10000

    def log(self, method: str, path: str, status_code: int, duration_ms: float,
            client_ip: str = None, user_agent: str = None, request_body: str = None) -> dict:
        entry = {
            "id": uuid.uuid4().hex[:12],
            "method": method,
            "path": path,
            "status_code": status_code,
            "duration_ms": round(duration_ms, 2),
            "client_ip": client_ip,
            "user_agent": user_agent,
            "created_at": datetime.now().isoformat(),
        }
        self._logs.append(entry)
        if len(self._logs) > self._max_size:
            self._logs = self._logs[-self._max_size:]
        return entry

    def list_logs(self, limit: int = 100, offset: int = 0, method: str = None,
                  status_code: int = None, path: str = None) -> List[dict]:
        logs = self._logs
        if method:
            logs = [l for l in logs if l["method"] == method.upper()]
        if status_code:
            logs = [l for l in logs if l["status_code"] == status_code]
        if path:
            logs = [l for l in logs if path.lower() in l["path"].lower()]
        logs = list(reversed(logs))
        return logs[offset:offset + limit]

    def get_count(self) -> int:
        return len(self._logs)
