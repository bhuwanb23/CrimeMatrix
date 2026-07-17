from typing import List, Dict, Optional
from identity.name_matcher import IndianNameMatcher
import structlog

logger = structlog.get_logger()


class EntityResolver:
    def __init__(self, name_threshold: int = 60):
        self.name_matcher = IndianNameMatcher()
        self.threshold = name_threshold

    def resolve_person(self, mention: str, candidates: List[Dict]) -> Optional[Dict]:
        if not candidates:
            return None

        best_match = None
        best_score = 0

        for candidate in candidates:
            name = candidate.get("name", "")
            if not name:
                continue
            result = self.name_matcher.match(mention, name)
            if result["score"] > best_score and result["score"] >= self.threshold:
                best_score = result["score"]
                best_match = {**candidate, "match_score": best_score, "match_type": result["match_type"]}

        return best_match

    def resolve_from_text(self, text: str, entities: List[Dict]) -> List[Dict]:
        results = []
        words = text.lower().split()

        for entity in entities:
            name = entity.get("name", "").lower()
            if not name:
                continue

            name_parts = name.split()
            overlap = sum(1 for part in name_parts if part in words)

            if overlap > 0:
                score = min(100, int((overlap / len(name_parts)) * 100))
                if score >= self.threshold:
                    results.append({
                        **entity,
                        "match_score": score,
                        "matched_parts": overlap,
                    })

        results.sort(key=lambda x: x["match_score"], reverse=True)
        return results

    def suggest_entity(self, partial_name: str, candidates: List[Dict],
                       top_k: int = 5) -> List[Dict]:
        suggestions = []
        for candidate in candidates:
            name = candidate.get("name", "")
            if not name:
                continue
            result = self.name_matcher.match(partial_name, name)
            if result["score"] >= 30:
                suggestions.append({
                    "name": name,
                    "score": result["score"],
                    "match_type": result["match_type"],
                    **{k: v for k, v in candidate.items() if k != "name"},
                })
        suggestions.sort(key=lambda x: x["score"], reverse=True)
        return suggestions[:top_k]
