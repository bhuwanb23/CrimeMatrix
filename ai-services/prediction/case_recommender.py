from typing import Dict, List, Optional
import structlog

logger = structlog.get_logger()


class CaseRecommendation:
    def recommend(self, target_case: Dict, all_cases: List[Dict], top_k: int = 5) -> List[Dict]:
        scored = []
        for case in all_cases:
            if case.get("id") == target_case.get("id"):
                continue
            score = self._score_similarity(target_case, case)
            if score > 0:
                scored.append({
                    "case_id": case.get("id"),
                    "title": case.get("title", ""),
                    "crime_type": case.get("crime_type", ""),
                    "district": case.get("district", ""),
                    "similarity_score": score,
                    "reasons": self._get_reasons(target_case, case),
                })
        scored.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored[:top_k]

    def recommend_next_steps(
        self,
        case: Dict,
        all_cases: List[Dict] = None,
        evidence: List[Dict] = None,
        officers: List[Dict] = None,
        investigations: List[Dict] = None,
    ) -> List[Dict]:
        steps = []

        if evidence:
            unlinked = [e for e in evidence if not e.get("linked")]
            if unlinked:
                steps.append({
                    "rec_type": "evidence_review",
                    "title": f"{len(unlinked)} evidence items need review",
                    "entity_type": "evidence",
                    "entity_id": unlinked[0].get("id", 0),
                    "score": min(90, len(unlinked) * 20),
                    "reasons": ["Unlinked evidence items in case"],
                })

        if officers and not case.get("assigned_officer"):
            best = max(officers, key=lambda o: o.get("caseload_capacity", 0) - o.get("current_load", 0))
            steps.append({
                "rec_type": "officer_assignment",
                "title": f"Suggest assigning Officer {best.get('name', 'Unknown')}",
                "entity_type": "officer",
                "entity_id": best.get("id", 0),
                "score": 75,
                "reasons": ["Available capacity, same district"],
            })

        if case.get("priority_score", 0) > 0.7:
            steps.append({
                "rec_type": "priority_escalation",
                "title": "High priority case needs escalation",
                "entity_type": "case",
                "entity_id": case.get("id", 0),
                "score": round(case["priority_score"] * 100, 1),
                "reasons": [f"Priority score {case['priority_score']:.0%}"],
            })

        if investigations:
            related = self._find_related_investigations(case, investigations)
            for inv in related[:2]:
                steps.append({
                    "rec_type": "related_investigation",
                    "title": f"Related: {inv.get('title', 'Investigation')}",
                    "entity_type": "investigation",
                    "entity_id": inv.get("id", 0),
                    "score": inv.get("relevance", 60),
                    "reasons": inv.get("reasons", []),
                })

        return sorted(steps, key=lambda x: x["score"], reverse=True)

    def _find_related_investigations(self, case: Dict, investigations: List[Dict]) -> List[Dict]:
        related = []
        for inv in investigations:
            reasons = []
            score = 0
            if inv.get("crime_type") == case.get("crime_type"):
                reasons.append(f"Same crime type: {case['crime_type']}")
                score += 30
            if inv.get("district") == case.get("district"):
                reasons.append(f"Same district: {case['district']}")
                score += 25
            shared_suspects = set(inv.get("suspect_ids", [])) & set(case.get("suspect_ids", []))
            if shared_suspects:
                reasons.append(f"{len(shared_suspects)} shared suspect(s)")
                score += 40
            if score > 0:
                related.append({"id": inv["id"], "title": inv.get("title"), "relevance": min(95, score), "reasons": reasons})
        return sorted(related, key=lambda x: x["relevance"], reverse=True)

    def _score_similarity(self, case1: Dict, case2: Dict) -> float:
        score = 0
        if case1.get("crime_type") == case2.get("crime_type"):
            score += 30
        if case1.get("district") == case2.get("district"):
            score += 20
        desc1 = set(case1.get("description", "").lower().split())
        desc2 = set(case2.get("description", "").lower().split())
        if desc1 and desc2:
            overlap = len(desc1 & desc2) / max(len(desc1 | desc2), 1)
            score += overlap * 30
        if case1.get("status") == case2.get("status"):
            score += 10
        return min(100, score)

    def _get_reasons(self, target: Dict, candidate: Dict) -> List[str]:
        reasons = []
        if target.get("crime_type") == candidate.get("crime_type"):
            reasons.append(f"Same crime type: {target.get('crime_type')}")
        if target.get("district") == candidate.get("district"):
            reasons.append(f"Same district: {target.get('district')}")
        if target.get("status") == candidate.get("status"):
            reasons.append(f"Same status: {target.get('status')}")
        return reasons
