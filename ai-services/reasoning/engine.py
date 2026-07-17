from typing import Dict, List
from reasoning.chain import ReasoningChainGenerator
from reasoning.evidence import EvidenceRanking
from reasoning.attribution import SourceAttribution
from reasoning.confidence import ConfidenceCalculator
from reasoning.explainability import ExplainabilityEngine
import structlog

logger = structlog.get_logger()


class ReasoningEngine:
    def __init__(self, provider: str = None, model: str = None):
        self.chain_gen = ReasoningChainGenerator()
        self.evidence_ranker = EvidenceRanking()
        self.attribution = SourceAttribution()
        self.confidence_calc = ConfidenceCalculator()
        self.explainer = ExplainabilityEngine(provider, model)

    async def analyze(self, hypothesis: str, evidence: List[Dict],
                       chain_type: str = "abductive") -> Dict:
        ranked_evidence = self.evidence_ranker.rank(evidence, hypothesis)
        chain = self.chain_gen.build(hypothesis, ranked_evidence, chain_type)
        confidence = self.confidence_calc.compute(chain)
        attributions = self.attribution.trace(chain)
        audit_trail = self.attribution.build_audit_trail(chain, attributions)
        explanation = await self.explainer.explain(chain, confidence)

        return {
            "hypothesis": hypothesis,
            "chain_type": chain_type,
            "chain": chain,
            "confidence": confidence,
            "attributions": attributions,
            "audit_trail": audit_trail,
            "explanation": explanation,
            "evidence_ranked": ranked_evidence,
        }

    def analyze_sync(self, hypothesis: str, evidence: List[Dict],
                      chain_type: str = "abductive") -> Dict:
        ranked_evidence = self.evidence_ranker.rank(evidence, hypothesis)
        chain = self.chain_gen.build(hypothesis, ranked_evidence, chain_type)
        confidence = self.confidence_calc.compute(chain)
        attributions = self.attribution.trace(chain)
        explanation = self.explainer._fallback_explain(chain, confidence)

        return {
            "hypothesis": hypothesis,
            "chain_type": chain_type,
            "chain": chain,
            "confidence": confidence,
            "attributions": attributions,
            "explanation": explanation,
        }

    def get_stats(self) -> dict:
        return {
            "evidence_types": list(EVIDENCE_STRENGTH.keys()) if hasattr(self.evidence_ranker, '_compute_score') else [],
            "confidence_levels": ["very_low", "low", "moderate", "high", "very_high"],
            "chain_types": ["deductive", "inductive", "abductive"],
        }


from reasoning.evidence import EVIDENCE_STRENGTH
