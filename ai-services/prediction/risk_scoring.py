from typing import Dict, List
import structlog

logger = structlog.get_logger()

DEFAULT_WEIGHTS = {
    "criminal_history": 0.25,
    "offense_severity": 0.20,
    "age_factor": 0.10,
    "location_risk": 0.15,
    "associate_risk": 0.15,
    "recency": 0.15,
}


class RiskScoring:
    def __init__(self, weights: Dict = None):
        self.weights = weights or DEFAULT_WEIGHTS

    def score(self, profile: Dict) -> Dict:
        factors = {}

        prior = profile.get("prior_offenses", 0)
        factors["criminal_history"] = min(1.0, prior / 10)

        severity_map = {"minor": 0.2, "moderate": 0.5, "serious": 0.7, "severe": 1.0}
        severity = profile.get("offense_severity", "moderate")
        factors["offense_severity"] = severity_map.get(severity, 0.5)

        age = profile.get("age", 30)
        if age < 25:
            factors["age_factor"] = 0.8
        elif age < 35:
            factors["age_factor"] = 0.6
        elif age < 50:
            factors["age_factor"] = 0.4
        else:
            factors["age_factor"] = 0.2

        high_risk_areas = profile.get("high_risk_areas", [])
        district = profile.get("district", "")
        factors["location_risk"] = 0.8 if district in high_risk_areas else 0.3

        associates_criminal = profile.get("associates_with_criminal_record", 0)
        factors["associate_risk"] = min(1.0, associates_criminal / 5)

        years = profile.get("years_since_last_offense", 5)
        factors["recency"] = max(0, 1.0 - years * 0.15)

        total = sum(factors[k] * self.weights[k] for k in factors)
        risk_score = round(total * 100, 1)

        level = "very_high" if risk_score >= 75 else "high" if risk_score >= 50 else "medium" if risk_score >= 25 else "low"

        return {
            "risk_score": risk_score,
            "risk_level": level,
            "factors": {k: round(v, 3) for k, v in factors.items()},
            "weights": self.weights,
            "breakdown": {k: round(factors[k] * self.weights[k] * 100, 1) for k in factors},
        }

    def compare(self, profiles: List[Dict]) -> List[Dict]:
        scored = [{"profile": p, **self.score(p)} for p in profiles]
        scored.sort(key=lambda x: x["risk_score"], reverse=True)
        return scored
