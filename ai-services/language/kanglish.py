from typing import Dict
import structlog

logger = structlog.get_logger()

KANGlish_KN = {
    "namaskara": "ನಮಸ್ಕಾರ", "namaskaram": "ನಮಸ್ಕಾರ",
    "howdu": "ಹೌದು", "illa": "ಇಲ್ಲ", "hogu": "ಹೋಗು",
    "baa": "ಬಾ", "iru": "ಇರು", "maadu": "ಮಾಡು",
    "thiliko": "ತಿಳಿಕೊ", "helu": "ಹೇಳು", "nodu": "ನೋಡು",
    "thindi": "ತಿಂಡಿ", "oota": "ಊಟ", "neeru": "ನೀರು",
    "mane": "ಮನೆ", "oora": "ಊರು", "daari": "ದಾರಿ",
    "polisi": "ಪೊಲೀಸ್", "kasu": "ಕಾಸು", "hushi": "ಹುಷಾರ್",
    "sari": "ಸರಿ", "beda": "ಬೇಡ", "beku": "ಬೇಕು",
    "illaa": "ಇಲ್ಲ", "aagilla": "ಆಗಿಲ್ಲ", "aaytu": "ಆಯ್ತು",
    "yenko": "ಎಂಕೆ", "yenu": "ಏನು", "yaaru": "ಯಾರು",
    "elli": "ಎಲ್ಲಿ", "yaavaga": "ಯಾವಾಗ", "hege": "ಹೇಗೆ",
    "yakendu": "ಯಾಕೆ", "sumne": "ಸುಮ್ಮನೆ", "chennagi": "ಚೆನ್ನಾಗಿ",
    "thumba": "ತುಂಬಾ", "swalpa": "ಸ್ವಲ್ಪ", "ille": "ಇಲ್ಲೇ",
    "illaa": "ಇಲ್ಲ", "barutte": "ಬರುತ್ತೆ", "hogutte": "ಹೋಗುತ್ತೆ",
}

KANGlish_EN = {
    "namaskara": "hello", "namaskaram": "hello",
    "howdu": "yes", "illa": "no", "hogu": "go",
    "baa": "come", "iru": "stay", "maadu": "do",
    "thiliko": "understand", "helu": "tell", "nodu": "see",
    "thindi": "snack", "oota": "food", "neeru": "water",
    "mane": "house", "oora": "village", "daari": "road",
    "polisi": "police", "kasu": "money", "hushi": "careful",
    "sari": "okay", "beda": "no want", "beku": "want",
    "yenko": "why", "yenu": "what", "yaaru": "who",
    "elli": "where", "yaavaga": "when", "hege": "how",
    "sumne": "quiet", "chennagi": "good", "thumba": "very",
    "swalpa": "little", "ille": "here",
}


class KanglishNormalizer:
    def normalize(self, text: str, target: str = "english") -> Dict:
        words = text.lower().split()
        detected_kanglish = [w for w in words if w in KANGlish_KN]

        if target == "kannada":
            normalized = [KANGlish_KN.get(w, w) for w in words]
        else:
            normalized = [KANGlish_EN.get(w, w) for w in words]

        return {
            "original": text,
            "normalized": " ".join(normalized),
            "target": target,
            "kanglish_detected": detected_kanglish,
            "is_kanglish": len(detected_kanglish) > 0,
        }

    def detect_script(self, text: str) -> str:
        kannada = sum(1 for c in text if 0x0C80 <= ord(c) <= 0x0CFF)
        if kannada > len(text) * 0.3:
            return "kannada"
        if any(w in KANGlish_KN for w in text.lower().split()):
            return "kanglish"
        return "english"

    def batch_normalize(self, texts: List[str], target: str = "english") -> List[Dict]:
        return [self.normalize(t, target) for t in texts]
