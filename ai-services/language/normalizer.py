import re
from typing import Dict, List
from language.kanglish import KanglishNormalizer
import structlog

logger = structlog.get_logger()

STOP_WORDS_EN = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at", "to", "for",
                 "of", "with", "by", "from", "and", "or", "but", "not", "this", "that", "it",
                 "be", "has", "have", "had", "do", "does", "did", "will", "would", "could",
                 "should", "may", "might", "can", "shall", "i", "you", "he", "she", "we", "they",
                 "near", "about", "around", "into", "over", "under", "after", "before"}

SYNONYMS = {
    "rob": ["robbery", "steal", "theft"],
    "steal": ["theft", "robbery", "larceny"],
    "kill": ["murder", "homicide"],
    "hit": ["assault", "attack"],
    "cheat": ["fraud", "scam"],
    "bengaluru": ["bangalore", "bengaluru", "bangalore"],
}


class QueryNormalizer:
    def __init__(self):
        self.kanglish = KanglishNormalizer()

    def normalize(self, query: str) -> Dict:
        normalized = query.lower().strip()
        normalized = re.sub(r'[^\w\s]', ' ', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()

        kanglish_result = self.kanglish.normalize(normalized, "english")
        if kanglish_result["is_kanglish"]:
            normalized = kanglish_result["normalized"]

        words = normalized.split()
        filtered = [w for w in words if w not in STOP_WORDS_EN]
        normalized = " ".join(filtered)

        expanded = self._expand_synonyms(normalized)

        return {
            "original": query,
            "normalized": normalized,
            "expanded": expanded,
            "kanglish_detected": kanglish_result["is_kanglish"],
            "word_count": len(filtered),
        }

    def _expand_synonyms(self, query: str) -> List[str]:
        words = query.split()
        expanded = set(words)
        for word in words:
            for key, syns in SYNONYMS.items():
                if word == key or word in syns:
                    expanded.update(syns)
        return list(expanded)

    def batch_normalize(self, queries: List[str]) -> List[Dict]:
        return [self.normalize(q) for q in queries]
