from typing import Dict, List
import structlog

logger = structlog.get_logger()


class RepeatOffenderPrediction:
    def predict(self, criminal_profile: Dict) -> Dict:
        prior_offenses = criminal_profile.get("prior_offenses", 0)
        age = criminal_profile.get("age", 30)
        risk_score = criminal_profile.get("risk_score", 0)
        years_since = criminal_profile.get("years_since_last_offense", 0)

        score = 0
        factors = []

        if prior_offenses >= 5:
            score += 35
            factors.append(f"High prior offenses ({prior_offenses})")
        elif prior_offenses >= 3:
            score += 25
            factors.append(f"Multiple prior offenses ({prior_offenses})")
        elif prior_offenses >= 1:
            score += 15
            factors.append(f"Some prior offenses ({prior_offenses})")

        if risk_score > 0.7:
            score += 20
            factors.append(f"High risk score ({risk_score:.2f})")
        elif risk_score > 0.4:
            score += 10
            factors.append(f"Moderate risk score ({risk_score:.2f})")

        if years_since <= 1:
            score += 20
            factors.append("Recent offense (within 1 year)")
        elif years_since <= 3:
            score += 10
            factors.append("Offense within 3 years")

        if age < 25:
            score += 10
            factors.append("Young age group")
        elif age > 50:
            score -= 10
            factors.append("Older age (lower recidivism)")

        score = max(0, min(100, score))
        level = "very_high" if score >= 70 else "high" if score >= 50 else "medium" if score >= 30 else "low"

        return {
            "risk_score": score,
            "risk_level": level,
            "factors": factors,
            "prior_offenses": prior_offenses,
            "recommendation": self._get_recommendation(level),
        }

    def _get_recommendation(self, level: str) -> str:
        recommendations = {
            "very_high": "Priority monitoring, regular check-ins, enhanced surveillance",
            "high": "Increased monitoring, periodic reviews",
            "medium": "Standard monitoring schedule",
            "low": "Routine check-ins",
        }
        return recommendations.get(level, "Standard procedure")

    def batch_predict(self, profiles: List[Dict]) -> List[Dict]:
        return [{**p, "prediction": self.predict(p)} for p in profiles]
