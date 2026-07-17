from typing import Dict, List
from datetime import datetime
import structlog

logger = structlog.get_logger()


class AccuracyTracker:
    def __init__(self):
        self._records: List[dict] = []

    def record(self, query: str, response: str, accuracy_score: float,
               domain: str = "general", metadata: dict = None):
        entry = {
            "query": query[:200],
            "response": response[:200],
            "accuracy_score": max(0, min(100, accuracy_score)),
            "domain": domain,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
        }
        self._records.append(entry)
        if len(self._records) > 5000:
            self._records = self._records[-5000:]

    def get_stats(self, domain: str = None) -> Dict:
        records = self._records
        if domain:
            records = [r for r in records if r["domain"] == domain]

        if not records:
            return {"total": 0, "avg_accuracy": 0, "min_accuracy": 0, "max_accuracy": 0}

        scores = [r["accuracy_score"] for r in records]
        return {
            "total": len(records),
            "avg_accuracy": round(sum(scores) / len(scores), 1),
            "min_accuracy": min(scores),
            "max_accuracy": max(scores),
        }

    def get_by_domain(self) -> Dict[str, Dict]:
        domains = {}
        for r in self._records:
            d = r["domain"]
            if d not in domains:
                domains[d] = {"scores": [], "count": 0}
            domains[d]["scores"].append(r["accuracy_score"])
            domains[d]["count"] += 1

        result = {}
        for d, data in domains.items():
            scores = data["scores"]
            result[d] = {
                "count": data["count"],
                "avg_accuracy": round(sum(scores) / len(scores), 1),
            }
        return result

    def get_recent(self, limit: int = 20) -> List[dict]:
        return list(reversed(self._records))[:limit]
