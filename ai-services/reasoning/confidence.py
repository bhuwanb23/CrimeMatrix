from typing import Dict, List
from datetime import datetime, timedelta
import math
import structlog

logger = structlog.get_logger()


class ConfidenceCalculator:
    def __init__(self, decay_rate: float = 0.01):
        self.decay_rate = decay_rate

    def compute(self, chain: Dict) -> Dict:
        steps = chain.get("steps", [])
        if not steps:
            return {"score": 0, "level": "none", "breakdown": {}}

        supporting = [s for s in steps if s.get("supports_hypothesis", True)]
        contradicting = [s for s in steps if not s.get("supports_hypothesis", True)]

        base_scores = [s.get("strength", 0.5) for s in supporting]
        base_confidence = sum(base_scores) / len(base_scores) if base_scores else 0

        time_adjusted = [self._apply_decay(s) for s in supporting]
        decay_adjusted = sum(time_adjusted) / len(time_adjusted) if time_adjusted else 0

        if len(supporting) >= 2:
            independent_boost = min(0.2, (len(supporting) - 1) * 0.05)
        else:
            independent_boost = 0

        contradiction_penalty = len(contradicting) * 0.15

        final = max(0, min(1.0, decay_adjusted + independent_boost - contradiction_penalty))
        score = round(final * 100, 1)

        return {
            "score": score,
            "level": self._score_to_level(score),
            "breakdown": {
                "base_confidence": round(base_confidence * 100, 1),
                "decay_adjusted": round(decay_adjusted * 100, 1),
                "independent_boost": round(independent_boost * 100, 1),
                "contradiction_penalty": round(contradiction_penalty * 100, 1),
                "supporting_count": len(supporting),
                "contradicting_count": len(contradicting),
            },
        }

    def _apply_decay(self, step: Dict) -> float:
        strength = step.get("strength", 0.5)
        date_str = step.get("date")
        if not date_str:
            return strength
        try:
            ev_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            days_ago = (datetime.now(ev_date.tzinfo) - ev_date).days
            decay = math.exp(-self.decay_rate * days_ago)
            return strength * decay
        except Exception:
            return strength

    def _score_to_level(self, score: float) -> str:
        if score >= 80:
            return "very_high"
        elif score >= 60:
            return "high"
        elif score >= 40:
            return "moderate"
        elif score >= 20:
            return "low"
        return "very_low"

    def compute_pairwise(self, evidence1: Dict, evidence2: Dict) -> float:
        s1 = evidence1.get("strength", 0.5)
        s2 = evidence2.get("strength", 0.5)
        return round(min(1.0, (s1 + s2) / 2 + 0.1), 3)
