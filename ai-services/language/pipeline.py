from language.translator import Translator
from language.kanglish import KanglishNormalizer
from language.normalizer import QueryNormalizer
import structlog

logger = structlog.get_logger()

KANNADA_RANGE = (0x0C80, 0x0CFF)
HINDI_RANGE = (0x0900, 0x097F)


class LanguagePipeline:
    def __init__(self):
        self.translator = Translator()
        self.kanglish = KanglishNormalizer()
        self.normalizer = QueryNormalizer()

    def detect_language(self, text: str) -> str:
        kannada = sum(1 for c in text if KANNADA_RANGE[0] <= ord(c) <= KANNADA_RANGE[1])
        hindi = sum(1 for c in text if HINDI_RANGE[0] <= ord(c) <= HINDI_RANGE[1])

        if kannada > len(text) * 0.2:
            return "kn"
        if hindi > len(text) * 0.2:
            return "hi"

        kanglish_result = self.kanglish.detect_script(text)
        if kanglish_result == "kanglish":
            return "kanglish"

        return "en"

    def process_input(self, text: str, user_language: str = "en") -> Dict:
        detected = self.detect_language(text)
        original_text = text
        processed_text = text

        if detected == "kanglish":
            kn_result = self.kanglish.normalize(text, "english")
            processed_text = kn_result["normalized"]
            detected = "en"
        elif detected == "kn":
            en_result = self.translator.translate(text, "kn", "en")
            processed_text = en_result["translated"]
        elif detected == "hi":
            processed_text = text

        query_result = self.normalizer.normalize(processed_text)
        normalized = query_result.get("normalized", processed_text)

        return {
            "original": original_text,
            "detected_language": detected,
            "normalized_query": normalized,
            "processed_text": processed_text,
            "user_language": user_language,
        }

    def process_output(self, text: str, target_language: str = "en") -> Dict:
        if target_language == "en":
            return {"text": text, "language": "en", "translated": False}

        if target_language == "kn":
            result = self.translator.translate(text, "en", "kn")
            return {"text": result["translated"], "language": "kn", "translated": True}

        return {"text": text, "language": target_language, "translated": False}


pipeline = LanguagePipeline()
