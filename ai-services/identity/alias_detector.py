from typing import List, Dict, Optional
from identity.name_matcher import IndianNameMatcher
import structlog

logger = structlog.get_logger()

# Common Indian alias/title patterns
TITLE_PATTERNS = {
    "bhai": "brother",
    "anna": "elder brother",
    "dada": "elder brother",
    "appa": "father",
    "amma": "mother",
    "akka": "elder sister",
    "thai": "mother",
    "master": "young man",
    "sir": "officer",
    "seth": "merchant",
    "chacha": "uncle",
    "mama": "uncle",
    "tau": "uncle",
}

# Common name abbreviations
ABBREVIATIONS = {
    "r": ["ram", "raju", "ravi", "raj"],
    "k": ["kumar", "krishna"],
    "s": ["singh", "sharma", "suresh"],
    "p": ["patel", "prasad"],
    "m": ["mohan", "manoj", "mahesh"],
    "g": ["gopi", "gopal"],
    "v": ["venu", "vinod", "vijay"],
}


class AliasDetector:
    def __init__(self):
        self.name_matcher = IndianNameMatcher()

    def detect_aliases(self, name: str, known_aliases: List[str] = None,
                        all_names: List[str] = None) -> List[Dict]:
        aliases = []
        name_lower = name.lower().strip()

        if known_aliases:
            for alias in known_aliases:
                score = self.name_matcher.match(name_lower, alias.lower())
                aliases.append({
                    "alias": alias,
                    "score": score["score"],
                    "type": "known",
                })

        if all_names:
            for other_name in all_names:
                if other_name.lower() == name_lower:
                    continue
                score = self.name_matcher.match(name_lower, other_name)
                if score["score"] >= 70:
                    aliases.append({
                        "alias": other_name,
                        "score": score["score"],
                        "type": score["match_type"],
                    })

        for pattern, meaning in TITLE_PATTERNS.items():
            if pattern in name_lower:
                aliases.append({
                    "alias": pattern,
                    "score": 100,
                    "type": "title",
                    "meaning": meaning,
                })

        for abbr, full_names in ABBREVIATIONS.items():
            parts = name_lower.split()
            if len(parts) == 1 and parts[0] == abbr:
                for full in full_names:
                    aliases.append({
                        "alias": full,
                        "score": 50,
                        "type": "abbreviation",
                    })

        seen = set()
        unique = []
        for a in aliases:
            key = a["alias"].lower()
            if key not in seen:
                seen.add(key)
                unique.append(a)

        unique.sort(key=lambda x: x["score"], reverse=True)
        return unique

    def suggest_aliases(self, name: str, count: int = 5) -> List[str]:
        suggestions = set()
        parts = name.lower().split()

        for part in parts:
            for short, longs in {
                "raj": ["rajesh", "rajendra"],
                "ram": ["ramesh", "ramachandra"],
                "mohan": ["mohanlal", "mohanesh"],
                "krishna": ["krishnappa", "krishnamurthy"],
                "sri": ["sridhar", "srinivas", "srikanth"],
            }.items():
                if part == short:
                    suggestions.update(longs)
                elif part in longs:
                    suggestions.add(short)

        if len(parts) > 1:
            first = parts[0]
            last = parts[-1]
            suggestions.add(f"{first} kumar")
            suggestions.add(f"{first}appa")
            suggestions.add(f"bhai {last}")

        return list(suggestions)[:count]
