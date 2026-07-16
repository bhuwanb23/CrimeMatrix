import uuid
from datetime import datetime
from typing import List
import structlog

logger = structlog.get_logger()


class ModelLogStore:
    def __init__(self):
        self._logs: List[dict] = []

    def log(self, provider: str, model: str, prompt_tokens: int = 0,
            completion_tokens: int = 0, duration_ms: float = 0,
            status: str = "success", error: str = None, metadata: dict = None) -> dict:
        entry = {
            "id": uuid.uuid4().hex[:12],
            "provider": provider,
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "duration_ms": round(duration_ms, 2),
            "status": status,
            "error": error,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
        }
        self._logs.append(entry)
        if len(self._logs) > 5000:
            self._logs = self._logs[-5000:]
        return entry

    def list_logs(self, limit: int = 100, offset: int = 0, provider: str = None,
                  status: str = None) -> List[dict]:
        logs = self._logs
        if provider:
            logs = [l for l in logs if l["provider"] == provider]
        if status:
            logs = [l for l in logs if l["status"] == status]
        return list(reversed(logs))[offset:offset + limit]

    def get_stats(self) -> dict:
        total = len(self._logs)
        if total == 0:
            return {"total_calls": 0, "total_tokens": 0, "avg_duration_ms": 0}
        total_tokens = sum(l.get("total_tokens", 0) for l in self._logs)
        avg_duration = round(sum(l["duration_ms"] for l in self._logs) / total, 2)
        success = sum(1 for l in self._logs if l["status"] == "success")
        return {
            "total_calls": total,
            "success": success,
            "failed": total - success,
            "total_tokens": total_tokens,
            "avg_duration_ms": avg_duration,
        }
