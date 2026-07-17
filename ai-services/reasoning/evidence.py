from typing import Dict, List
from datetime import datetime, timedelta
import structlog

logger = structlog.get_logger()

EVIDENCE_STRENGTH = {
    "direct": 1.0,
    "physical": 0.9,
    "testimonial": 0.7,
    "circumstantial": 0.5,
    "hearsay": 0.3,
    "inference": 0.4,
}


class EvidenceRanking:
    def rank(self, evidence_list: List[Dict], hypothesis: str = None) -> List[Dict]:
        ranked = []
        for ev in evidence_list:
            score = self._compute_score(ev, hypothesis)
            ranked.append({**ev, "relevance_score": score})

        ranked.sort(key=lambda x: x["relevance_score"], reverse=True)
        return ranked

    def _compute_score(self, evidence: Dict, hypothesis: str = None) -> float:
        strength_score = EVIDENCE_STRENGTH.get(evidence.get("strength", "circumstantial"), 0.5)
        freshness_score = self._freshness_score(evidence.get("date"))
        type_bonus = 0.1 if evidence.get("corroborated") else 0
        relevance = evidence.get("relevance", 0.5)

        final = strength_score * 0.35 + freshness_score * 0.2 + relevance * 0.35 + type_bonus
        return round(min(1.0, final), 3)

    def _freshness_score(self, date_str: str = None) -> float:
        if not date_str:
            return 0.5
        try:
            ev_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            days_ago = (datetime.now(ev_date.tzinfo) - ev_date).days
            if days_ago <= 7:
                return 1.0
            elif days_ago <= 30:
                return 0.8
            elif days_ago <= 90:
                return 0.6
            elif days_ago <= 365:
                return 0.4
            return 0.2
        except Exception:
            return 0.5

    def get_top_evidence(self, evidence_list: List[Dict], top_k: int = 5) -> List[Dict]:
        return self.rank(evidence_list)[:top_k]

    def group_by_type(self, evidence_list: List[Dict]) -> Dict[str, List[Dict]]:
        groups = {}
        for ev in evidence_list:
            t = ev.get("type", "unknown")
            if t not in groups:
                groups[t] = []
            groups[t].append(ev)
        return groups
