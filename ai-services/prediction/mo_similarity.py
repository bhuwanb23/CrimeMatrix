from typing import Dict, List
import re
import structlog

logger = structlog.get_logger()

MO_KEYWORDS = {
    "entry": ["break", "window", "door", "lock", "force", "pry", "drill"],
    "time": ["night", "morning", "evening", "dawn", "dusk", "late", "early"],
    "weapon": ["knife", "gun", "weapon", "threat", "force", "violence"],
    "target": ["jewelry", "cash", "electronics", "vehicle", "phone", "wallet"],
    "method": ["snatch", "grab", "con", "trick", "ambush", "distraction"],
    "transport": ["bike", "car", "walk", "bus", "auto", "escape"],
}


class MOSimilarity:
    def compare(self, mo1: str, mo2: str) -> Dict:
        keywords1 = self._extract_keywords(mo1)
        keywords2 = self._extract_keywords(mo2)

        overlap = set(keywords1) & set(keywords2)
        union = set(keywords1) | set(keywords2)
        jaccard = len(overlap) / len(union) if union else 0

        categories1 = self._categorize(mo1)
        categories2 = self._categorize(mo2)
        cat_overlap = set(categories1.keys()) & set(categories2.keys())
        cat_score = len(cat_overlap) / max(len(set(categories1.keys()) | set(categories2.keys())), 1)

        overall = round((jaccard * 0.5 + cat_score * 0.5) * 100, 1)

        return {
            "similarity_score": overall,
            "keyword_overlap": list(overlap),
            "shared_categories": list(cat_overlap),
            "mo1_keywords": keywords1[:10],
            "mo2_keywords": keywords2[:10],
            "match_level": "strong" if overall > 70 else "moderate" if overall > 40 else "weak",
        }

    def _extract_keywords(self, text: str) -> List[str]:
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        stopwords = {"the", "and", "was", "for", "that", "with", "they", "from", "have", "this", "were", "been", "said"}
        return [w for w in words if w not in stopwords]

    def _categorize(self, text: str) -> Dict[str, int]:
        text_lower = text.lower()
        categories = {}
        for cat, keywords in MO_KEYWORDS.items():
            count = sum(1 for kw in keywords if kw in text_lower)
            if count > 0:
                categories[cat] = count
        return categories

    def find_similar_mos(self, target_mo: str, mo_list: List[Dict], top_k: int = 5) -> List[Dict]:
        results = []
        for mo in mo_list:
            comparison = self.compare(target_mo, mo.get("description", ""))
            results.append({
                "case_id": mo.get("case_id"),
                "description": mo.get("description", "")[:200],
                "similarity_score": comparison["similarity_score"],
                "match_level": comparison["match_level"],
                "shared_categories": comparison["shared_categories"],
            })
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:top_k]
