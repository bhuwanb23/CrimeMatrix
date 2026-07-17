import time
from typing import Dict, List
from collections import defaultdict
import structlog

logger = structlog.get_logger()


class LatencyTracker:
    def __init__(self):
        self._records: List[dict] = []
        self._active: Dict[str, float] = {}

    def start(self, request_id: str):
        self._active[request_id] = time.time()

    def end(self, request_id: str, endpoint: str = "", provider: str = "") -> float:
        start_time = self._active.pop(request_id, time.time())
        duration_ms = round((time.time() - start_time) * 1000, 2)
        self._records.append({
            "request_id": request_id,
            "endpoint": endpoint,
            "provider": provider,
            "duration_ms": duration_ms,
            "timestamp": datetime.now().isoformat(),
        })
        if len(self._records) > 10000:
            self._records = self._records[-10000:]
        return duration_ms

    def get_stats(self, endpoint: str = None) -> Dict:
        records = self._records
        if endpoint:
            records = [r for r in records if r["endpoint"] == endpoint]

        if not records:
            return {"count": 0, "avg_ms": 0, "p50": 0, "p95": 0, "p99": 0, "max_ms": 0}

        durations = sorted(r["duration_ms"] for r in records)
        n = len(durations)

        return {
            "count": n,
            "avg_ms": round(sum(durations) / n, 2),
            "p50": durations[n // 2],
            "p95": durations[int(n * 0.95)] if n > 1 else durations[0],
            "p99": durations[int(n * 0.99)] if n > 1 else durations[0],
            "max_ms": durations[-1],
            "min_ms": durations[0],
        }

    def get_slow_requests(self, threshold_ms: float = 5000) -> List[dict]:
        return [r for r in self._records if r["duration_ms"] > threshold_ms]

    def get_records(self, limit: int = 100) -> List[dict]:
        return list(reversed(self._records))[:limit]


from datetime import datetime
