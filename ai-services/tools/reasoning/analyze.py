import json
from tools.base import Tool


class ReasoningAnalyzeTool(Tool):
    def __init__(self):
        self._engine = None

    def _get_engine(self):
        if self._engine is None:
            from reasoning.engine import ReasoningEngine
            self._engine = ReasoningEngine(provider="ollama", model="llama3.2:1b")
        return self._engine

    def get_name(self) -> str:
        return "reasoning_analyze"

    def get_description(self) -> str:
        return "Perform chain-of-thought reasoning: generate reasoning chain, rank evidence, compute confidence, and explain the conclusion."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "hypothesis": {"type": "string", "description": "The hypothesis to evaluate (e.g., 'Suspect X is involved in the crime')"},
                "evidence": {"type": "array", "description": "List of evidence items, each with 'claim', 'type', 'strength', 'supports'"},
                "chain_type": {"type": "string", "description": "Reasoning type: 'deductive', 'inductive', or 'abductive'", "default": "abductive"},
            },
            "required": ["hypothesis", "evidence"],
        }

    async def execute(self, hypothesis: str = "", evidence: list = None,
                      chain_type: str = "abductive", **kwargs) -> str:
        engine = self._get_engine()
        result = await engine.analyze(hypothesis, evidence or [], chain_type)
        return json.dumps(result, default=str)
