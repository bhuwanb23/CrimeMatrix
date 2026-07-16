import time
from datetime import datetime
from typing import Dict
from collections import defaultdict
import structlog

logger = structlog.get_logger()


class MetricsEngine:
    def __init__(self):
        self._counters: Dict[str, int] = defaultdict(int)
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, list] = defaultdict(list)
        self._start_time = time.time()

    def increment(self, name: str, value: int = 1):
        self._counters[name] += value

    def decrement(self, name: str, value: int = 1):
        self._counters[name] -= value

    def set_gauge(self, name: str, value: float):
        self._gauges[name] = value

    def observe(self, name: str, value: float):
        self._histograms[name].append(value)
        if len(self._histograms[name]) > 1000:
            self._histograms[name] = self._histograms[name][-1000:]

    def get_counter(self, name: str) -> int:
        return self._counters.get(name, 0)

    def get_gauge(self, name: str) -> float:
        return self._gauges.get(name, 0)

    def get_histogram(self, name: str) -> dict:
        values = self._histograms.get(name, [])
        if not values:
            return {"count": 0, "min": 0, "max": 0, "avg": 0, "p50": 0, "p95": 0, "p99": 0}
        sorted_v = sorted(values)
        count = len(sorted_v)
        return {
            "count": count,
            "min": round(sorted_v[0], 2),
            "max": round(sorted_v[-1], 2),
            "avg": round(sum(sorted_v) / count, 2),
            "p50": round(sorted_v[count // 2], 2),
            "p95": round(sorted_v[int(count * 0.95)], 2) if count > 1 else round(sorted_v[0], 2),
            "p99": round(sorted_v[int(count * 0.99)], 2) if count > 1 else round(sorted_v[0], 2),
        }

    def get_all_metrics(self) -> dict:
        uptime = round(time.time() - self._start_time, 2)
        return {
            "uptime_seconds": uptime,
            "counters": dict(self._counters),
            "gauges": dict(self._gauges),
            "histograms": {name: self.get_histogram(name) for name in self._histograms},
        }

    def get_summary(self) -> dict:
        return {
            "uptime_seconds": round(time.time() - self._start_time, 2),
            "total_counters": len(self._counters),
            "total_gauges": len(self._gauges),
            "total_histograms": len(self._histograms),
            "counters": dict(self._counters),
            "gauges": dict(self._gauges),
        }
