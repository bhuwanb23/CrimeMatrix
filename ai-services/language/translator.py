from typing import Dict, List
import structlog

logger = structlog.get_logger()

EN_KN_DICT = {
    "hello": "ನಮಸ್ಕಾರ", "hi": "ನಮಸ್ಕಾರ", "thank": "ಧನ್ಯವಾದ", "thanks": "ಧನ್ಯವಾದ",
    "yes": "ಹೌದು", "no": "ಇಲ್ಲ", "good": "ಒಳ್ಳೆಯ", "bad": "ಕೆಟ್ಟ",
    "police": "ಪೊಲೀಸ್", "crime": "ಅಪರಾಧ", "theft": "ಕಳ್ಳತನ", "murder": "ಕೊಲೆ",
    "robbery": "ದರೋಡೆ", "fraud": "ವಂಚನೆ", "case": "ಪ್ರಕರಣ", "evidence": "ಸಾಕ್ಷ್ಯ",
    "suspect": "ಶಂಕಿತ", "victim": "ಬಾಧಿತ", "witness": "ಸಾಕ್ಷಿ", "officer": "ಅಧಿಕಾರಿ",
    "station": "ಠಾಣೆ", "district": "ಜಿಲ್ಲೆ", "report": "ವರದಿ", "file": "ಫೈಲ್",
    "search": "ಹುಡುಕು", "find": "ಹುಡುಕು", "help": "ಸಹಾಯ", "please": "ದಯವಿಟ್ಟು",
    "name": "ಹೆಸರು", "address": "ವಿಳಾಸ", "phone": "ಫೋನ್", "vehicle": "ವಾಹನ",
    "location": "ಸ್ಥಳ", "time": "ಸಮಯ", "date": "ದಿನಾಂಕ", "today": "ಇಂದು",
    "yesterday": "ನಿನ್ನೆ", "tomorrow": "ನಾಳೆ", "who": "ಯಾರು", "what": "ಏನು",
    "where": "ಎಲ್ಲಿ", "when": "ಯಾವಾಗ", "why": "ಯಾಕೆ", "how": "ಹೇಗೆ",
}

KN_EN_DICT = {v: k for k, v in EN_KN_DICT.items()}
KN_EN_DICT.update({
    "ನಮಸ್ಕಾರ": "hello", "ಹೌದು": "yes", "ಇಲ್ಲ": "no", "ಧನ್ಯವಾದ": "thank you",
    "ಪೊಲೀಸ್": "police", "ಅಪರಾಧ": "crime", "ಕಳ್ಳತನ": "theft", "ಕೊಲೆ": "murder",
    "ದರೋಡೆ": "robbery", "ಪ್ರಕರಣ": "case", "ಸಾಕ್ಷ್ಯ": "evidence",
    "ಶಂಕಿತ": "suspect", "ಬಾಧಿತ": "victim", "ಸಾಕ್ಷಿ": "witness",
    "ಠಾಣೆ": "station", "ಜಿಲ್ಲೆ": "district", "ವರದಿ": "report",
    "ಹುಡುಕು": "search", "ಸಹಾಯ": "help", "ದಯವಿಟ್ಟು": "please",
})


class Translator:
    def translate(self, text: str, source_lang: str = "auto", target_lang: str = "en") -> Dict:
        detected = source_lang if source_lang != "auto" else self._detect(text)

        if detected == target_lang:
            return {"original": text, "translated": text, "source": detected, "target": target_lang, "method": "same_lang"}

        if detected == "en" and target_lang == "kn":
            translated = self._en_to_kn(text)
        elif detected == "kn" and target_lang == "en":
            translated = self._kn_to_en(text)
        else:
            translated = text

        return {
            "original": text,
            "translated": translated,
            "source": detected,
            "target": target_lang,
            "method": "dictionary",
        }

    def _en_to_kn(self, text: str) -> str:
        words = text.lower().split()
        translated = [EN_KN_DICT.get(w, w) for w in words]
        return " ".join(translated)

    def _kn_to_en(self, text: str) -> str:
        words = text.split()
        translated = [KN_EN_DICT.get(w, w) for w in words]
        return " ".join(translated)

    def _detect(self, text: str) -> str:
        kannada = sum(1 for c in text if 0x0C80 <= ord(c) <= 0x0CFF)
        if kannada > len(text) * 0.3:
            return "kn"
        return "en"

    def batch_translate(self, texts: List[str], source_lang: str = "auto",
                         target_lang: str = "en") -> List[Dict]:
        return [self.translate(t, source_lang, target_lang) for t in texts]
