import re
from typing import List, Dict, Tuple
import structlog

logger = structlog.get_logger()

# Indian nickname/shortname mappings
NICKNAMES = {
    "raj": ["rajesh", "rajendra", "rajiv", "rajan", "rajani"],
    "raju": ["rajesh", "rajendra", "rajiv"],
    "mohan": ["mohanlal", "mohanraj", "mohanesh"],
    "kumar": ["kumaran", "kumara"],
    "ram": ["ramesh", "ramachandra", "ramakrishna", "ramya"],
    "shri": ["shridhar", "shrinivas", "shripal"],
    "sri": ["sridhar", "srinivas", "srikanth"],
    "gopi": ["gopalkrishna", "gopinath"],
    "venu": ["venugopal", "venkatesh"],
    "krishna": ["krishnappa", "krishnamurthy"],
    "suresh": ["suresh"],
    "mahesh": ["mahesh"],
    "dinesh": ["dinesh"],
    "rajesh": ["rajesh", "raj"],
    "ravi": ["ravindra", "ravikumar"],
    "anil": ["anil", "anilkumar"],
    "sunil": ["sunil"],
    "manoj": ["manoj", "manohar"],
    "vinod": ["vinod", "vinayak"],
}

# Common Indian surname patterns
SURNAMES = {
    "singh": ["singh", "sinh"],
    "kumar": ["kumar", "kumaran"],
    "patel": ["patel", "patil"],
    "sharma": ["sharma"],
    "reddy": ["reddy", "reddi"],
    "gowda": ["gowda", "gowdar"],
    "rao": ["rao", "raju"],
    "nair": ["nair", "nayar"],
    "iyer": ["iyer", "aiyer"],
    "shetty": ["shetty", "setty"],
}


class IndianNameMatcher:
    def __init__(self):
        self._build_reverse_nicknames()

    def _build_reverse_nicknames(self):
        self._reverse_nicknames = {}
        for short, longs in NICKNAMES.items():
            for long_name in longs:
                if long_name not in self._reverse_nicknames:
                    self._reverse_nicknames[long_name] = set()
                self._reverse_nicknames[long_name].add(short)
                self._reverse_nicknames[long_name].update(longs)

    def _normalize(self, name: str) -> str:
        name = name.lower().strip()
        name = re.sub(r'[^a-z\s]', '', name)
        name = re.sub(r'\s+', ' ', name)
        return name

    def _vowel_normalize(self, name: str) -> str:
        replacements = {'aa': 'a', 'ii': 'i', 'uu': 'u', 'ee': 'i', 'oo': 'u'}
        for old, new in replacements.items():
            name = name.replace(old, new)
        return name

    def _get_parts(self, name: str) -> List[str]:
        return self._normalize(name).split()

    def _soundex(self, name: str) -> str:
        name = self._normalize(name)
        if not name:
            return ""
        soundex = name[0]
        mapping = {
            'b': '1', 'f': '1', 'p': '1', 'v': '1',
            'c': '2', 'g': '2', 'j': '2', 'k': '2', 'q': '2', 's': '2', 'x': '2', 'z': '2',
            'd': '3', 't': '3',
            'l': '4',
            'm': '5', 'n': '5',
            'r': '6',
        }
        prev = mapping.get(name[0], '0')
        for char in name[1:]:
            code = mapping.get(char, '0')
            if code != '0' and code != prev:
                soundex += code
            prev = code
        return (soundex + '0000')[:4]

    def _is_nickname_pair(self, name1: str, name2: str) -> bool:
        n1 = self._normalize(name1)
        n2 = self._normalize(name2)
        if n1 in self._reverse_nicknames and n2 in self._reverse_nicknames.get(n1, set()):
            return True
        if n2 in self._reverse_nicknames and n1 in self._reverse_nicknames.get(n2, set()):
            return True
        return False

    def match(self, name1: str, name2: str) -> Dict:
        n1 = self._normalize(name1)
        n2 = self._normalize(name2)

        if n1 == n2:
            return {"score": 100, "match_type": "exact", "details": "Exact match"}

        parts1 = self._get_parts(name1)
        parts2 = self._get_parts(name2)

        exact_parts = set(parts1) & set(parts2)
        part_score = (len(exact_parts) / max(len(parts1), len(parts2))) * 100 if parts1 and parts2 else 0

        prefix_bonus = 0
        for p1 in parts1:
            for p2 in parts2:
                if len(p1) >= 3 and p2.startswith(p1):
                    prefix_bonus = max(prefix_bonus, 40)
                elif len(p2) >= 3 and p1.startswith(p2):
                    prefix_bonus = max(prefix_bonus, 40)

        nickname_bonus = 0
        for p1 in parts1:
            for p2 in parts2:
                if self._is_nickname_pair(p1, p2):
                    nickname_bonus = max(nickname_bonus, 30)

        soundex1 = self._soundex(name1)
        soundex2 = self._soundex(name2)
        phonetic_match = soundex1 == soundex2
        phonetic_bonus = 20 if phonetic_match else 0

        vn1 = self._vowel_normalize(n1)
        vn2 = self._vowel_normalize(n2)
        vowel_bonus = 10 if vn1 == vn2 and n1 != n2 else 0

        surname_bonus = 0
        for s, variants in SURNAMES.items():
            if any(p in variants for p in parts1) and any(p in variants for p in parts2):
                surname_bonus = 10
                break

        final_score = min(100, int(part_score + prefix_bonus + nickname_bonus + phonetic_bonus + vowel_bonus + surname_bonus))

        match_type = "exact" if final_score == 100 else \
                     "nickname" if nickname_bonus > 0 else \
                     "phonetic" if phonetic_match else \
                     "partial" if final_score > 50 else \
                     "weak" if final_score > 20 else "no_match"

        return {
            "score": final_score,
            "match_type": match_type,
            "details": f"Parts: {part_score:.0f}, Nickname: {nickname_bonus}, Phonetic: {phonetic_bonus}",
        }

    def batch_match(self, name: str, candidates: List[str], threshold: int = 50) -> List[Dict]:
        results = []
        for candidate in candidates:
            m = self.match(name, candidate)
            if m["score"] >= threshold:
                results.append({"name": candidate, **m})
        results.sort(key=lambda x: x["score"], reverse=True)
        return results
