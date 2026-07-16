import uuid
from datetime import datetime
from typing import List, Dict
from collections import defaultdict
import structlog

logger = structlog.get_logger()


class APILogStore:
    def __init__(self):
        self._logs: List[dict] = []
        self._counts: Dict[str, int] = defaultdict(int)
        self._status_counts: Dict[int, int] = defaultdict(int)

    def log(self, method: str, path: str, status_code: int, duration_ms: float,
            client_ip: str = None) -> dict:
        entry = {
            "id": uuid.uuid4().hex[:12],
            "method": method,
            "path": path,
            "status_code": status_code,
            "duration_ms": round(duration_ms, 2),
            "client_ip": client_ip,
            "created_at": datetime.now().isoformat(),
        }
        self._logs.append(entry)
        key = f"{method} {path}"
        self._counts[key] += 1
        self._status_counts[status_code] += 1
        if len(self._logs) > 10000:
            self._logs = self._logs[-10000:]
        return entry

    def get_summary(self) -> dict:
        total = len(self._logs)
        endpoints = sorted(self._counts.items(), key=lambda x: x[1], reverse=True)[:20]
        avg_duration = 0
        if self._logs:
            avg_duration = round(sum(l["duration_ms"] for l in self._logs) / total, 2)
        return {
            "total_requests": total,
            "top_endpoints": [{"endpoint": k, "count": v} for k, v in endpoints],
            "status_distribution": dict(self._status_counts),
            "avg_duration_ms": avg_duration,
        }

    def list_logs(self, limit: int = 100, offset: int = 0, method: str = None,
                  status_code: int = None) -> List[dict]:
        logs = self._logs
        if method:
            logs = [l for l in logs if l["method"] == method.upper()]
        if status_code:
            logs = [l for l in logs if l["status_code"] == status_code]
        return list(reversed(logs))[offset:offset + limit]
