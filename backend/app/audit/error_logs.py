import uuid
import traceback
from datetime import datetime
from typing import List
import structlog

logger = structlog.get_logger()


class ErrorLogStore:
    def __init__(self):
        self._logs: List[dict] = []

    def log(self, error_type: str, message: str, path: str = None,
            method: str = None, status_code: int = 500,
            stack_trace: str = None, details: dict = None) -> dict:
        entry = {
            "id": uuid.uuid4().hex[:12],
            "error_type": error_type,
            "message": message,
            "path": path,
            "method": method,
            "status_code": status_code,
            "stack_trace": stack_trace,
            "details": details or {},
            "created_at": datetime.now().isoformat(),
        }
        self._logs.append(entry)
        if len(self._logs) > 5000:
            self._logs = self._logs[-5000:]
        return entry

    def list_logs(self, limit: int = 100, offset: int = 0, error_type: str = None,
                  status_code: int = None) -> List[dict]:
        logs = self._logs
        if error_type:
            logs = [l for l in logs if l["error_type"] == error_type]
        if status_code:
            logs = [l for l in logs if l["status_code"] == status_code]
        return list(reversed(logs))[offset:offset + limit]

    def get_count(self) -> int:
        return len(self._logs)
