from typing import List, Dict, Tuple
from identity.name_matcher import IndianNameMatcher
import structlog

logger = structlog.get_logger()


class DuplicateDetector:
    def __init__(self):
        self.name_matcher = IndianNameMatcher()
        self.name_threshold = 80
        self.phone_exact = True

    def _normalize_phone(self, phone: str) -> str:
        return "".join(c for c in phone if c.isdigit())[-10:]

    def _normalize_district(self, district: str) -> str:
        return district.lower().strip() if district else ""

    def find_duplicates(self, records: List[Dict], id_key: str = "id") -> List[Dict]:
        duplicates = []
        for i in range(len(records)):
            for j in range(i + 1, len(records)):
                r1, r2 = records[i], records[j]
                score, reason = self._compare(r1, r2)
                if score >= self.name_threshold:
                    duplicates.append({
                        "record_1": r1.get(id_key),
                        "record_2": r2.get(id_key),
                        "score": score,
                        "reason": reason,
                        "name_1": r1.get("name", ""),
                        "name_2": r2.get("name", ""),
                    })
        duplicates.sort(key=lambda x: x["score"], reverse=True)
        return duplicates

    def _compare(self, r1: Dict, r2: Dict) -> Tuple[int, str]:
        reasons = []
        total_score = 0

        name1 = r1.get("name", "")
        name2 = r2.get("name", "")
        if name1 and name2:
            name_result = self.name_matcher.match(name1, name2)
            if name_result["score"] > 50:
                total_score = max(total_score, name_result["score"])
                reasons.append(f"name: {name_result['match_type']} ({name_result['score']})")

        phone1 = self._normalize_phone(str(r1.get("phone", "")))
        phone2 = self._normalize_phone(str(r2.get("phone", "")))
        if phone1 and phone2 and phone1 == phone2:
            total_score = max(total_score, 95)
            reasons.append("exact phone match")

        age1 = r1.get("age")
        age2 = r2.get("age")
        if age1 and age2 and abs(int(age1) - int(age2)) <= 2:
            total_score = max(total_score, total_score + 10)
            reasons.append("age within 2 years")

        d1 = self._normalize_district(str(r1.get("district", "")))
        d2 = self._normalize_district(str(r2.get("district", "")))
        if d1 and d2 and d1 == d2:
            reasons.append("same district")

        return min(100, total_score), "; ".join(reasons) if reasons else "no match"
