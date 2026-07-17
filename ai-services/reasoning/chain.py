from typing import Dict, List
from datetime import datetime
import structlog

logger = structlog.get_logger()


class ReasoningChainGenerator:
    def build(self, hypothesis: str, evidence: List[Dict], chain_type: str = "abductive") -> Dict:
        steps = []
        supporting = [e for e in evidence if e.get("supports", True)]
        contradicting = [e for e in evidence if not e.get("supports", True)]

        for i, ev in enumerate(supporting):
            strength = ev.get("strength", 0.5)
            steps.append({
                "step_id": i + 1,
                "claim": ev.get("claim", f"Evidence piece {i+1}"),
                "evidence_id": ev.get("id", f"evidence_{i}"),
                "evidence_type": ev.get("type", "circumstantial"),
                "strength": strength,
                "supports_hypothesis": True,
                "description": ev.get("description", ""),
            })

        for i, ev in enumerate(contradicting):
            strength = ev.get("strength", 0.5)
            steps.append({
                "step_id": len(supporting) + i + 1,
                "claim": ev.get("claim", f"Contradicting evidence {i+1}"),
                "evidence_id": ev.get("id", f"evidence_c_{i}"),
                "evidence_type": ev.get("type", "circumstantial"),
                "strength": strength,
                "supports_hypothesis": False,
                "description": ev.get("description", ""),
            })

        if chain_type == "deductive":
            conclusion = self._deductive_conclusion(hypothesis, steps)
        elif chain_type == "inductive":
            conclusion = self._inductive_conclusion(hypothesis, steps)
        else:
            conclusion = self._abductive_conclusion(hypothesis, steps)

        return {
            "hypothesis": hypothesis,
            "chain_type": chain_type,
            "steps": steps,
            "conclusion": conclusion,
            "total_evidence": len(evidence),
            "supporting_count": len(supporting),
            "contradicting_count": len(contradicting),
            "created_at": datetime.now().isoformat(),
        }

    def _deductive_conclusion(self, hypothesis: str, steps: list) -> Dict:
        supporting = [s for s in steps if s["supports_hypothesis"]]
        avg_strength = sum(s["strength"] for s in supporting) / len(supporting) if supporting else 0
        all_strong = all(s["strength"] >= 0.7 for s in supporting) if supporting else False

        return {
            "verdict": "supported" if all_strong and len(supporting) >= 2 else "inconclusive",
            "reasoning": f"All {len(supporting)} supporting evidence items are strong (avg: {avg_strength:.2f})" if all_strong else "Evidence is insufficient or mixed",
            "strength": avg_strength,
        }

    def _inductive_conclusion(self, hypothesis: str, steps: list) -> Dict:
        supporting = [s for s in steps if s["supports_hypothesis"]]
        pattern_count = len([s for s in supporting if s["evidence_type"] in ("historical", "pattern")])

        return {
            "verdict": "probable" if len(supporting) >= 3 else "possible",
            "reasoning": f"{len(supporting)} evidence pieces support the hypothesis, {pattern_count} show pattern",
            "strength": min(1.0, len(supporting) * 0.15 + pattern_count * 0.1),
        }

    def _abductive_conclusion(self, hypothesis: str, steps: list) -> Dict:
        supporting = [s for s in steps if s["supports_hypothesis"]]
        contradicting = [s for s in steps if not s["supports_hypothesis"]]
        net_support = len(supporting) - len(contradicting)

        return {
            "verdict": "best_explanation" if net_support >= 2 else "alternative_explanation",
            "reasoning": f"Net {net_support} evidence items favor the hypothesis",
            "strength": max(0, min(1.0, net_support * 0.2)),
        }
