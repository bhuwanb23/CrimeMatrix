from typing import Dict, List
from collections import defaultdict
from datetime import datetime
import structlog

logger = structlog.get_logger()

COST_PER_1K_TOKENS = {
    "ollama": 0.0,
    "openai": {"gpt-4o-mini": 0.00015, "gpt-4o": 0.005, "gpt-3.5-turbo": 0.0001},
    "gemini": {"gemini-2.0-flash": 0.000075, "gemini-2.0-pro": 0.00125},
}


class CostTracker:
    def __init__(self):
        self._records: List[dict] = []

    def record(self, provider: str, model: str, prompt_tokens: int,
               completion_tokens: int, request_id: str = ""):
        cost = self._calculate_cost(provider, model, prompt_tokens, completion_tokens)
        entry = {
            "provider": provider,
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "cost_usd": cost,
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
        }
        self._records.append(entry)
        if len(self._records) > 10000:
            self._records = self._records[-10000:]

    def _calculate_cost(self, provider: str, model: str, prompt_tokens: int,
                         completion_tokens: int) -> float:
        if provider == "ollama":
            return 0.0
        rates = COST_PER_1K_TOKENS.get(provider, {})
        if isinstance(rates, dict):
            rate = rates.get(model, 0.001)
        else:
            rate = rates
        return round((prompt_tokens + completion_tokens) / 1000 * rate, 6)

    def get_stats(self) -> Dict:
        if not self._records:
            return {"total_cost": 0, "total_requests": 0, "avg_cost": 0}
        total = sum(r["cost_usd"] for r in self._records)
        return {
            "total_cost_usd": round(total, 6),
            "total_requests": len(self._records),
            "avg_cost_per_request": round(total / len(self._records), 6) if self._records else 0,
        }

    def get_by_provider(self) -> Dict[str, Dict]:
        by_provider = defaultdict(lambda: {"cost": 0, "tokens": 0, "calls": 0})
        for r in self._records:
            p = r["provider"]
            by_provider[p]["cost"] += r["cost_usd"]
            by_provider[p]["tokens"] += r["total_tokens"]
            by_provider[p]["calls"] += 1
        return {k: {**v, "cost_usd": round(v["cost"], 6)} for k, v in by_provider.items()}

    def get_daily(self, days: int = 7) -> List[Dict]:
        daily = defaultdict(lambda: {"cost": 0, "tokens": 0, "calls": 0})
        for r in self._records:
            day = r["timestamp"][:10]
            daily[day]["cost"] += r["cost_usd"]
            daily[day]["tokens"] += r["total_tokens"]
            daily[day]["calls"] += 1
        return [{"date": k, "cost_usd": round(v["cost"], 6), **v} for k, v in sorted(daily.items())[-days:]]
