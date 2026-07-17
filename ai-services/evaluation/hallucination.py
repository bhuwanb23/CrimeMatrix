from datetime import datetime
from typing import Dict, List
import re
import structlog

logger = structlog.get_logger()


class HallucinationDetector:
    def __init__(self):
        self._records: List[dict] = []

    def check(self, response: str, evidence: List[Dict] = None,
              context: str = "") -> Dict:
        claims = self._extract_claims(response)
        supported = []
        unsupported = []

        evidence_text = " ".join(e.get("content", "") for e in (evidence or []))
        evidence_text += " " + context

        for claim in claims:
            if self._is_supported(claim, evidence_text):
                supported.append(claim)
            else:
                unsupported.append(claim)

        total = len(claims)
        supported_count = len(supported)
        hallucination_rate = (len(unsupported) / total * 100) if total > 0 else 0

        result = {
            "total_claims": total,
            "supported_claims": supported_count,
            "unsupported_claims": len(unsupported),
            "hallucination_rate": round(hallucination_rate, 1),
            "supported": supported[:5],
            "unsupported": unsupported[:5],
            "verdict": "clean" if hallucination_rate < 10 else "warning" if hallucination_rate < 30 else "high_risk",
        }

        self._records.append({**result, "timestamp": datetime.now().isoformat()})
        return result

    def _extract_claims(self, text: str) -> List[str]:
        sentences = re.split(r'[.!?]+', text)
        claims = [s.strip() for s in sentences if len(s.strip()) > 10]
        return claims[:20]

    def _is_supported(self, claim: str, evidence: str) -> bool:
        claim_words = set(claim.lower().split())
        evidence_words = set(evidence.lower().split())
        overlap = len(claim_words & evidence_words)
        return overlap >= len(claim_words) * 0.3

    def get_stats(self) -> Dict:
        if not self._records:
            return {"total_checks": 0, "avg_hallucination_rate": 0}
        avg_rate = sum(r["hallucination_rate"] for r in self._records) / len(self._records)
        return {
            "total_checks": len(self._records),
            "avg_hallucination_rate": round(avg_rate, 1),
            "clean_rate": round(100 - avg_rate, 1),
        }
