import time
from datetime import datetime
from typing import Dict, List
from collections import defaultdict


class TokenTracker:
    def __init__(self):
        self._calls: List[dict] = []
        self._totals: Dict[str, dict] = defaultdict(lambda: {"calls": 0, "tokens": 0, "duration_ms": 0})

    def record(self, provider: str, model: str, prompt_tokens: int, completion_tokens: int,
               duration_ms: float, status: str = "success"):
        entry = {
            "provider": provider,
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "duration_ms": round(duration_ms, 2),
            "status": status,
            "timestamp": datetime.now().isoformat(),
        }
        self._calls.append(entry)
        key = f"{provider}/{model}"
        self._totals[key]["calls"] += 1
        self._totals[key]["tokens"] += entry["total_tokens"]
        self._totals[key]["duration_ms"] += duration_ms
        if len(self._calls) > 5000:
            self._calls = self._calls[-5000:]
        return entry

    def get_usage(self, provider: str = None, limit: int = 100) -> list:
        calls = self._calls
        if provider:
            calls = [c for c in calls if c["provider"] == provider]
        return list(reversed(calls))[:limit]

    def get_totals(self) -> dict:
        return dict(self._totals)

    def get_summary(self) -> dict:
        total_calls = len(self._calls)
        total_tokens = sum(c["total_tokens"] for c in self._calls)
        total_duration = sum(c["duration_ms"] for c in self._calls)
        return {
            "total_calls": total_calls,
            "total_tokens": total_tokens,
            "total_duration_ms": round(total_duration, 2),
            "avg_duration_ms": round(total_duration / total_calls, 2) if total_calls else 0,
            "by_provider": dict(self._totals),
        }


token_tracker = TokenTracker()
