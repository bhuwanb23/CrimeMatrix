from typing import Dict
from core.provider import registry as provider_registry
import structlog

logger = structlog.get_logger()

EXPLAIN_PROMPT = """You are a criminal intelligence analyst explaining a reasoning chain.

Hypothesis: {hypothesis}

Reasoning Chain:
{chain_summary}

Confidence: {confidence}% ({confidence_level})

Generate a clear, professional explanation of how this conclusion was reached.
Structure it as:
1. What was investigated
2. Key evidence found
3. How evidence connects to the hypothesis
4. Confidence level and what it means

Keep it under 300 words. Use bullet points for evidence items."""


class ExplainabilityEngine:
    def __init__(self, provider: str = None, model: str = None):
        self.provider_name = provider
        self.model_name = model

    async def explain(self, chain: Dict, confidence: Dict) -> str:
        chain_summary = self._format_chain(chain)
        prompt = EXPLAIN_PROMPT.format(
            hypothesis=chain.get("hypothesis", ""),
            chain_summary=chain_summary,
            confidence=confidence.get("score", 0),
            confidence_level=confidence.get("level", "unknown"),
        )

        try:
            provider = provider_registry.get(self.provider_name)
            response = await provider.chat(
                [{"role": "user", "content": prompt}],
                model=self.model_name,
            )
            return response.strip()
        except Exception as e:
            logger.error("explainability_error", error=str(e))
            return self._fallback_explain(chain, confidence)

    def _format_chain(self, chain: Dict) -> str:
        lines = []
        for step in chain.get("steps", []):
            support = "supports" if step.get("supports_hypothesis", True) else "contradicts"
            lines.append(f"- Step {step.get('step_id')}: {step.get('claim')} ({support}, strength: {step.get('strength', 0)})")
        return "\n".join(lines)

    def _fallback_explain(self, chain: Dict, confidence: Dict) -> str:
        hypothesis = chain.get("hypothesis", "the hypothesis")
        supporting = [s for s in chain.get("steps", []) if s.get("supports_hypothesis", True)]
        contradicting = [s for s in chain.get("steps", []) if not s.get("supports_hypothesis", True)]

        parts = [
            f"**Analysis of: {hypothesis}**",
            f"",
            f"**Evidence supporting ({len(supporting)} items):**",
        ]
        for s in supporting:
            parts.append(f"- {s.get('claim', 'Unknown')} (strength: {s.get('strength', 0):.0%})")

        if contradicting:
            parts.append(f"")
            parts.append(f"**Contradicting evidence ({len(contradicting)} items):**")
            for s in contradicting:
                parts.append(f"- {s.get('claim', 'Unknown')} (strength: {s.get('strength', 0):.0%})")

        parts.append(f"")
        parts.append(f"**Confidence: {confidence.get('score', 0)}% ({confidence.get('level', 'unknown')})**")

        return "\n".join(parts)
