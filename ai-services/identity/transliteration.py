from typing import Dict, Optional
import structlog

logger = structlog.get_logger()

# Kannada Unicode range: 0C80-0CFF
# Devanagari (Hindi) Unicode range: 0900-097F

KANNADA_TO_ENGLISH = {
    'ಕ': 'ka', 'ಖ': 'kha', 'ಗ': 'ga', 'ಘ': 'gha', 'ಙ': 'nga',
    'ಚ': 'cha', 'ಛ': 'chha', 'ಜ': 'ja', 'ಝ': 'jha', 'ಞ': 'nya',
    'ಟ': 'ta', 'ಠ': 'tha', 'ಡ': 'da', 'ಢ': 'dha', 'ಣ': 'na',
    'ತ': 'ta', 'ಥ': 'tha', 'ದ': 'da', 'ಧ': 'dha', 'ನ': 'na',
    'ಪ': 'pa', 'ಫ': 'pha', 'ಬ': 'ba', 'ಭ': 'bha', 'ಮ': 'ma',
    'ಯ': 'ya', 'ರ': 'ra', 'ಲ': 'la', 'ವ': 'va', 'ಶ': 'sha',
    'ಷ': 'sha', 'ಸ': 'sa', 'ಹ': 'ha', 'ಳ': 'la', 'ಕ್ಷ': 'ksha',
    'ಜ್ಞ': 'gya',
    'ಾ': 'aa', 'ಿ': 'i', 'ೀ': 'ee', 'ು': 'u', 'ೂ': 'oo',
    'ೃ': 'ru', 'ೆ': 'e', 'ೇ': 'ee', 'ೈ': 'ai', 'ೊ': 'o',
    'ೋ': 'oo', 'ೌ': 'au', 'ಂ': 'n', 'ಃ': 'h', '್': '',
}

DEVANAGARI_TO_ENGLISH = {
    'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ee', 'उ': 'u', 'ऊ': 'oo',
    'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
    'क': 'ka', 'ख': 'kha', 'ग': 'ga', 'घ': 'gha', 'ङ': 'nga',
    'च': 'cha', 'छ': 'chha', 'ज': 'ja', 'झ': 'jha', 'ञ': 'nya',
    'ट': 'ta', 'ठ': 'tha', 'ड': 'da', 'ढ': 'dha', 'ण': 'na',
    'त': 'ta', 'थ': 'tha', 'द': 'da', 'ध': 'dha', 'न': 'na',
    'प': 'pa', 'फ': 'pha', 'ब': 'ba', 'भ': 'bha', 'म': 'ma',
    'य': 'ya', 'र': 'ra', 'ल': 'la', 'व': 'va', 'श': 'sha',
    'ष': 'sha', 'स': 'sa', 'ह': 'ha', 'ळ': 'la',
    'ा': 'aa', 'ि': 'i', 'ी': 'ee', 'ु': 'u', 'ू': 'oo',
    'ृ': 'ru', 'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au',
    'ं': 'n', 'ः': 'h', '्': '',
}

# Reverse: English to Kannada (best-effort phonetic)
ENGLISH_TO_KANNADA = {
    'ka': 'ಕ', 'kha': 'ಖ', 'ga': 'ಗ', 'gha': 'ಘ',
    'cha': 'ಚ', 'ja': 'ಜ', 'ta': 'ತ', 'da': 'ದ',
    'na': 'ನ', 'pa': 'ಪ', 'ba': 'ಬ', 'ma': 'ಮ',
    'ya': 'ಯ', 'ra': 'ರ', 'la': 'ಲ', 'va': 'ವ',
    'sha': 'ಶ', 'sa': 'ಸ', 'ha': 'ಹ',
    'a': 'ಅ', 'i': 'ಇ', 'u': 'ಉ', 'e': 'ಎ', 'o': 'ಒ',
}


class TransliterationEngine:
    def detect_script(self, text: str) -> str:
        for char in text:
            cp = ord(char)
            if 0x0C80 <= cp <= 0x0CFF:
                return "kannada"
            if 0x0900 <= cp <= 0x097F:
                return "devanagari"
        return "latin"

    def kannada_to_english(self, text: str) -> str:
        result = []
        i = 0
        while i < len(text):
            found = False
            for length in [2, 1]:
                chunk = text[i:i+length]
                if chunk in KANNADA_TO_ENGLISH:
                    result.append(KANNADA_TO_ENGLISH[chunk])
                    i += length
                    found = True
                    break
            if not found:
                result.append(text[i])
                i += 1
        return "".join(result).strip()

    def devanagari_to_english(self, text: str) -> str:
        result = []
        i = 0
        while i < len(text):
            found = False
            for length in [2, 1]:
                chunk = text[i:i+length]
                if chunk in DEVANAGARI_TO_ENGLISH:
                    result.append(DEVANAGARI_TO_ENGLISH[chunk])
                    i += length
                    found = True
                    break
            if not found:
                result.append(text[i])
                i += 1
        return "".join(result).strip()

    def english_to_kannada(self, text: str) -> str:
        text = text.lower()
        result = []
        i = 0
        while i < len(text):
            found = False
            for length in [3, 2, 1]:
                chunk = text[i:i+length]
                if chunk in ENGLISH_TO_KANNADA:
                    result.append(ENGLISH_TO_KANNADA[chunk])
                    i += length
                    found = True
                    break
            if not found:
                result.append(text[i])
                i += 1
        return "".join(result)

    def transliterate(self, text: str, target: str = "english") -> Dict:
        script = self.detect_script(text)
        if target == "english":
            if script == "kannada":
                return {"original": text, "script": "kannada", "result": self.kannada_to_english(text), "target": "english"}
            elif script == "devanagari":
                return {"original": text, "script": "devanagari", "result": self.devanagari_to_english(text), "target": "english"}
            return {"original": text, "script": "latin", "result": text, "target": "english"}
        elif target == "kannada":
            return {"original": text, "script": script, "result": self.english_to_kannada(text), "target": "kannada"}
        return {"original": text, "script": script, "result": text, "target": target}
