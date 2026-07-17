import pytest
from reasoning.chain import ReasoningChainGenerator
from reasoning.evidence import EvidenceRanking, EVIDENCE_STRENGTH
from reasoning.attribution import SourceAttribution
from reasoning.confidence import ConfidenceCalculator
from reasoning.explainability import ExplainabilityEngine
from reasoning.engine import ReasoningEngine


SAMPLE_EVIDENCE = [
    {"id": "e1", "claim": "Vehicle matching suspect's car found at scene", "type": "physical", "strength": 0.9, "supports": True},
    {"id": "e2", "claim": "Phone records show suspect near location", "type": "direct", "strength": 0.85, "supports": True},
    {"id": "e3", "claim": "Witness saw someone matching description", "type": "testimonial", "strength": 0.6, "supports": True},
    {"id": "e4", "claim": "Suspect was out of town according to alibi", "type": "testimonial", "strength": 0.5, "supports": False},
]


class TestReasoningChainGenerator:
    def setup_method(self):
        self.gen = ReasoningChainGenerator()

    def test_build_chain(self):
        chain = self.gen.build("Suspect is involved", SAMPLE_EVIDENCE)
        assert chain["hypothesis"] == "Suspect is involved"
        assert len(chain["steps"]) == 4
        assert chain["supporting_count"] == 3
        assert chain["contradicting_count"] == 1

    def test_deductive_chain(self):
        chain = self.gen.build("Suspect is involved", SAMPLE_EVIDENCE, "deductive")
        assert chain["chain_type"] == "deductive"
        assert "verdict" in chain["conclusion"]

    def test_inductive_chain(self):
        chain = self.gen.build("Suspect is involved", SAMPLE_EVIDENCE, "inductive")
        assert chain["chain_type"] == "inductive"

    def test_abductive_chain(self):
        chain = self.gen.build("Suspect is involved", SAMPLE_EVIDENCE, "abductive")
        assert chain["chain_type"] == "abductive"
        assert chain["conclusion"]["verdict"] in ("best_explanation", "alternative_explanation")

    def test_empty_evidence(self):
        chain = self.gen.build("Hypothesis", [])
        assert len(chain["steps"]) == 0
        assert chain["supporting_count"] == 0


class TestEvidenceRanking:
    def setup_method(self):
        self.ranker = EvidenceRanking()

    def test_rank_by_strength(self):
        ranked = self.ranker.rank(SAMPLE_EVIDENCE)
        assert ranked[0]["relevance_score"] >= ranked[-1]["relevance_score"]

    def test_top_evidence(self):
        top = self.ranker.get_top_evidence(SAMPLE_EVIDENCE, top_k=2)
        assert len(top) == 2

    def test_group_by_type(self):
        groups = self.ranker.group_by_type(SAMPLE_EVIDENCE)
        assert "physical" in groups
        assert "direct" in groups

    def test_strength_map(self):
        assert EVIDENCE_STRENGTH["direct"] == 1.0
        assert EVIDENCE_STRENGTH["hearsay"] == 0.3


class TestSourceAttribution:
    def setup_method(self):
        self.attr = SourceAttribution()

    def test_trace(self):
        chain = ReasoningChainGenerator().build("Hypothesis", SAMPLE_EVIDENCE)
        attributions = self.attr.trace(chain)
        assert len(attributions) == 4
        assert all("trace_id" in a for a in attributions)

    def test_reliability(self):
        assert self.attr._source_reliability("direct") == 0.95
        assert self.attr._source_reliability("hearsay") == 0.3

    def test_audit_trail(self):
        chain = ReasoningChainGenerator().build("Hypothesis", SAMPLE_EVIDENCE)
        attributions = self.attr.trace(chain)
        trail = self.attr.build_audit_trail(chain, attributions)
        assert "overall_reliability" in trail
        assert trail["total_steps"] == 4


class TestConfidenceCalculator:
    def setup_method(self):
        self.calc = ConfidenceCalculator()

    def test_compute_with_evidence(self):
        chain = ReasoningChainGenerator().build("Hypothesis", SAMPLE_EVIDENCE)
        conf = self.calc.compute(chain)
        assert conf["score"] > 0
        assert conf["level"] in ("very_low", "low", "moderate", "high", "very_high")
        assert "breakdown" in conf

    def test_empty_chain(self):
        conf = self.calc.compute({"steps": []})
        assert conf["score"] == 0
        assert conf["level"] == "none"

    def test_all_supporting(self):
        evidence = [
            {"claim": "A", "strength": 0.9, "supports": True},
            {"claim": "B", "strength": 0.8, "supports": True},
        ]
        chain = ReasoningChainGenerator().build("H", evidence)
        conf = self.calc.compute(chain)
        assert conf["score"] > 50

    def test_contradiction_penalty(self):
        evidence = [
            {"claim": "A", "strength": 0.8, "supports": True},
            {"claim": "B", "strength": 0.7, "supports": False},
            {"claim": "C", "strength": 0.6, "supports": False},
        ]
        chain = ReasoningChainGenerator().build("H", evidence)
        conf = self.calc.compute(chain)
        assert conf["breakdown"]["contradiction_penalty"] > 0

    def test_score_to_level(self):
        assert self.calc._score_to_level(90) == "very_high"
        assert self.calc._score_to_level(70) == "high"
        assert self.calc._score_to_level(50) == "moderate"
        assert self.calc._score_to_level(30) == "low"
        assert self.calc._score_to_level(10) == "very_low"


class TestExplainabilityEngine:
    def test_fallback_explain(self):
        engine = ExplainabilityEngine()
        chain = ReasoningChainGenerator().build("Hypothesis", SAMPLE_EVIDENCE)
        confidence = ConfidenceCalculator().compute(chain)
        explanation = engine._fallback_explain(chain, confidence)
        assert "Hypothesis" in explanation or "hypothesis" in explanation.lower()
        assert "evidence" in explanation.lower()


class TestReasoningEngine:
    def setup_method(self):
        self.engine = ReasoningEngine()

    def test_analyze_sync(self):
        result = self.engine.analyze_sync("Suspect X is involved", SAMPLE_EVIDENCE)
        assert "chain" in result
        assert "confidence" in result
        assert "explanation" in result
        assert result["confidence"]["score"] > 0

    def test_stats(self):
        stats = self.engine.get_stats()
        assert "chain_types" in stats
        assert "confidence_levels" in stats
