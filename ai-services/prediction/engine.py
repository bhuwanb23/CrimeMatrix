from typing import Dict, List
from prediction.crime_forecast import CrimeForecasting
from prediction.hotspot import HotspotPrediction
from prediction.repeat_offender import RepeatOffenderPrediction
from prediction.risk_scoring import RiskScoring
from prediction.mo_similarity import MOSimilarity
from prediction.case_recommender import CaseRecommendation
import structlog

logger = structlog.get_logger()


class PredictionEngine:
    def __init__(self):
        self.forecast = CrimeForecasting()
        self.hotspot = HotspotPrediction()
        self.repeat_offender = RepeatOffenderPrediction()
        self.risk = RiskScoring()
        self.mo = MOSimilarity()
        self.recommender = CaseRecommendation()

    async def predict(self, prediction_type: str, data: Dict) -> Dict:
        if prediction_type == "forecast":
            return self.forecast.forecast(data.get("historical", []), data.get("periods_ahead", 1))
        elif prediction_type == "hotspots":
            return {"hotspots": self.hotspot.identify_hotspots(data.get("crimes", []), data.get("top_n", 5))}
        elif prediction_type == "recidivism":
            return self.repeat_offender.predict(data.get("profile", {}))
        elif prediction_type == "risk":
            return self.risk.score(data.get("profile", {}))
        elif prediction_type == "mo_similarity":
            return self.mo.compare(data.get("mo1", ""), data.get("mo2", ""))
        elif prediction_type == "cases":
            return {"recommendations": self.recommender.recommend(data.get("case", {}), data.get("all_cases", []))}
        else:
            return {"error": f"Unknown prediction type: {prediction_type}"}

    def get_stats(self) -> dict:
        return {
            "prediction_types": ["forecast", "hotspots", "recidivism", "risk", "mo_similarity", "cases"],
            "components": 6,
        }
