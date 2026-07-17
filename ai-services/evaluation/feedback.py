from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict
import structlog

logger = structlog.get_logger()


class FeedbackLoop:
    def __init__(self):
        self._feedback: List[dict] = []

    def submit(self, rating: int, query: str, response: str = "",
               session_id: str = "default", comment: str = None,
               tags: List[str] = None):
        entry = {
            "rating": max(1, min(5, rating)),
            "query": query[:500],
            "response": response[:500],
            "session_id": session_id,
            "comment": comment,
            "tags": tags or [],
            "timestamp": datetime.now().isoformat(),
        }
        self._feedback.append(entry)
        if len(self._feedback) > 5000:
            self._feedback = self._feedback[-5000:]

    def get_stats(self) -> Dict:
        if not self._feedback:
            return {"total": 0, "avg_rating": 0, "distribution": {}}

        ratings = [f["rating"] for f in self._feedback]
        dist = defaultdict(int)
        for r in ratings:
            dist[r] += 1

        positive = sum(1 for r in ratings if r >= 4)
        negative = sum(1 for r in ratings if r <= 2)

        return {
            "total": len(ratings),
            "avg_rating": round(sum(ratings) / len(ratings), 2),
            "distribution": dict(dist),
            "positive_rate": round(positive / len(ratings) * 100, 1),
            "negative_rate": round(negative / len(ratings) * 100, 1),
        }

    def get_by_tags(self) -> Dict[str, Dict]:
        by_tag = defaultdict(list)
        for f in self._feedback:
            for tag in f.get("tags", []):
                by_tag[tag].append(f["rating"])

        return {
            tag: {
                "count": len(ratings),
                "avg_rating": round(sum(ratings) / len(ratings), 2),
            }
            for tag, ratings in by_tag.items()
        }

    def get_recent(self, limit: int = 20) -> List[dict]:
        return list(reversed(self._feedback))[:limit]

    def get_negative_feedback(self, limit: int = 20) -> List[dict]:
        negative = [f for f in self._feedback if f["rating"] <= 2]
        return list(reversed(negative))[:limit]
