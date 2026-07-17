from typing import Dict, List
from collections import defaultdict
from datetime import datetime, timedelta
import structlog

logger = structlog.get_logger()


class TokenTracker:
    def __init__(self):
        self._records: List[dict] = []

    def record(self, provider: str, model: str, prompt_tokens: int,
               completion_tokens: int, session_id: str = "default"):
        entry = {
            "provider": provider,
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
        }
        self._records.append(entry)
        if len(self._records) > 10000:
            self._records = self._records[-10000:]

    def get_stats(self, provider: str = None) -> Dict:
        records = self._records
        if provider:
            records = [r for r in records if r["provider"] == provider]

        if not records:
            return {"total_calls": 0, "total_tokens": 0, "avg_tokens": 0}

        total_prompt = sum(r["prompt_tokens"] for r in records)
        total_completion = sum(r["completion_tokens"] for r in records)
        total = total_prompt + total_completion

        return {
            "total_calls": len(records),
            "total_prompt_tokens": total_prompt,
            "total_completion_tokens": total_completion,
            "total_tokens": total,
            "avg_tokens_per_call": round(total / len(records)),
        }

    def get_by_provider(self) -> Dict[str, Dict]:
        by_provider = defaultdict(list)
        for r in self._records:
            by_provider[r["provider"]].append(r)

        result = {}
        for provider, records in by_provider.items():
            total = sum(r["total_tokens"] for r in records)
            result[provider] = {
                "calls": len(records),
                "total_tokens": total,
                "avg_tokens": round(total / len(records)),
            }
        return result

    def get_daily(self, days: int = 7) -> List[Dict]:
        daily = defaultdict(lambda: {"calls": 0, "tokens": 0})
        for r in self._records:
            day = r["timestamp"][:10]
            daily[day]["calls"] += 1
            daily[day]["tokens"] += r["total_tokens"]
        return [{"date": k, **v} for k, v in sorted(daily.items())[-days:]]
