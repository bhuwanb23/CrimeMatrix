import uuid
from datetime import datetime
from typing import List
import structlog

logger = structlog.get_logger()


class SystemLogStore:
    def __init__(self):
        self._logs: List[dict] = []

    def log(self, level: str, message: str, component: str = "system", details: dict = None) -> dict:
        entry = {
            "id": uuid.uuid4().hex[:12],
            "level": level,
            "message": message,
            "component": component,
            "details": details or {},
            "created_at": datetime.now().isoformat(),
        }
        self._logs.append(entry)
        if len(self._logs) > 5000:
            self._logs = self._logs[-5000:]
        return entry

    def info(self, message: str, **kwargs):
        return self.log("info", message, **kwargs)

    def warning(self, message: str, **kwargs):
        return self.log("warning", message, **kwargs)

    def error(self, message: str, **kwargs):
        return self.log("error", message, **kwargs)

    def debug(self, message: str, **kwargs):
        return self.log("debug", message, **kwargs)

    def list_logs(self, limit: int = 100, offset: int = 0, level: str = None) -> List[dict]:
        logs = self._logs
        if level:
            logs = [l for l in logs if l["level"] == level.lower()]
        return list(reversed(logs))[offset:offset + limit]
