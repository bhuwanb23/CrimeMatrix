from typing import Dict, List
import structlog

logger = structlog.get_logger()


class CaseRecommendation:
    def recommend(self, target_case: Dict, all_cases: List[Dict], top_k: int = 5) -> List[Dict]:
        target_type = target_case.get("crime_type", "")
        target_location = target_case.get("district", "")
        target_mo = target_case.get("description", "").lower()

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
