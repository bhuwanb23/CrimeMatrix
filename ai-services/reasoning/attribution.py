from typing import Dict, List
from datetime import datetime
import structlog

logger = structlog.get_logger()


class SourceAttribution:
    def trace(self, chain: Dict) -> List[Dict]:
        attributions = []
        for step in chain.get("steps", []):
            attribution = {
                "step_id": step.get("step_id"),
                "claim": step.get("claim"),
                "source_id": step.get("evidence_id"),
                "source_type": step.get("evidence_type", "unknown"),
                "reliability": self._source_reliability(step.get("evidence_type")),
                "trace_id": f"trace_{step.get('step_id', 0)}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            }
            attributions.append(attribution)
        return attributions

    def _source_reliability(self, source_type: str) -> float:
        reliability_map = {
            "direct": 0.95,
            "physical": 0.9,
            "document": 0.85,
            "testimonial": 0.7,
            "circumstantial": 0.5,
            "hearsay": 0.3,
            "inference": 0.4,
        }
        return reliability_map.get(source_type, 0.5)

    def build_audit_trail(self, chain: Dict, attributions: List[Dict]) -> Dict:
        return {
            "hypothesis": chain.get("hypothesis"),
            "chain_type": chain.get("chain_type"),
            "total_steps": len(chain.get("steps", [])),
            "attributions": attributions,
            "overall_reliability": sum(a["reliability"] for a in attributions) / len(attributions) if attributions else 0,
            "generated_at": datetime.now().isoformat(),
        }
