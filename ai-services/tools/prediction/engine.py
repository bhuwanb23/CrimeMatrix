import json
from tools.base import Tool


class PredictionEngineTool(Tool):
    def __init__(self):
        self._engine = None

    def _get_engine(self):
        if self._engine is None:
            from prediction.engine import PredictionEngine
            self._engine = PredictionEngine()
        return self._engine

    def get_name(self) -> str:
        return "prediction_engine"

    def get_description(self) -> str:
        return "Predict crime patterns: forecast trends, identify hotspots, assess recidivism risk, score risk, match MO patterns, recommend similar cases."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "prediction_type": {"type": "string", "description": "Type: 'forecast', 'hotspots', 'recidivism', 'risk', 'mo_similarity', 'cases'"},
                "data": {"type": "object", "description": "Input data for the prediction"},
            },
            "required": ["prediction_type", "data"],
        }

    async def execute(self, prediction_type: str = "", data: dict = None, **kwargs) -> str:
        engine = self._get_engine()
        result = await engine.predict(prediction_type, data or {})
        return json.dumps(result, default=str)
