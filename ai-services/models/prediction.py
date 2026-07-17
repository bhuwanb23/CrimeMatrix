from typing import Dict
from prediction.engine import PredictionEngine
from models.registry import model_registry
import structlog

logger = structlog.get_logger()


class PredictionModel:
    def __init__(self):
        self._engine = PredictionEngine()

    async def predict(self, prediction_type: str, data: Dict, model: str = None) -> Dict:
        return await self._engine.predict(prediction_type, data)

    def get_config(self) -> Dict:
        return {
            "available_types": ["forecast", "hotspots", "recidivism", "risk", "mo_similarity", "cases"],
            "engine": "rule_based",
        }
