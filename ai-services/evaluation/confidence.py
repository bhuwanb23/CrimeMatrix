from typing import Dict, List
from collections import defaultdict
from datetime import datetime
import structlog

logger = structlog.get_logger()


class ConfidenceTracker:
    def __init__(self):
        self._records: List[dict] = []

    def record(self, confidence_score: float, query: str = "",
               context: str = None, was_correct: bool = None):
        entry = {
            "confidence": confidence_score,
            "query": query[:200],
            "context": context,
            "was_correct": was_correct,
            "timestamp": datetime.now().isoformat(),
        }
        self._records.append(entry)
        if len(self._records) > 5000:
            self._records = self._records[-5000:]

    def get_distribution(self) -> Dict:
        if not self._records:
            return {"count": 0, "distribution": {}}

        buckets = {"0-20": 0, "20-40": 0, "40-60": 0, "60-80": 0, "80-100": 0}
        for r in self._records:
            c = r["confidence"]
            if c < 20:
                buckets["0-20"] += 1
            elif c < 40:
                buckets["20-40"] += 1
            elif c < 60:
                buckets["40-60"] += 1
            elif c < 80:
                buckets["60-80"] += 1
            else:
                buckets["80-100"] += 1

        return {"count": len(self._records), "distribution": buckets}

    def get_calibration(self) -> Dict:
        scored = [r for r in self._records if r.get("was_correct") is not None]
        if not scored:
            return {"calibration_data": [], "note": "No labeled data for calibration"}

        calibration = defaultdict(lambda: {"total": 0, "correct": 0})
        for r in scored:
            bucket = round(r["confidence"] / 10) * 10
            calibration[bucket]["total"] += 1
            if r["was_correct"]:
                calibration[bucket]["correct"] += 1

        result = []
        for bucket in sorted(calibration.keys()):
            data = calibration[bucket]
            actual_accuracy = round(data["correct"] / data["total"] * 100, 1) if data["total"] else 0
            result.append({
                "confidence_bucket": f"{bucket}-{bucket+10}",
                "expected": bucket + 5,
                "actual": actual_accuracy,
                "samples": data["total"],
            })

        return {"calibration_data": result}

    def get_stats(self) -> Dict:
        if not self._records:
            return {"count": 0, "avg_confidence": 0}
        scores = [r["confidence"] for r in self._records]
        return {
            "count": len(scores),
            "avg_confidence": round(sum(scores) / len(scores), 1),
            "min_confidence": min(scores),
            "max_confidence": max(scores),
        }
