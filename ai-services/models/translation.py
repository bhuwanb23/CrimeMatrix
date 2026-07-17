from typing import Dict
from language.translator import Translator
from language.kanglish import KanglishNormalizer
from models.registry import model_registry
import structlog

logger = structlog.get_logger()


class TranslationModel:
    def __init__(self):
        self._translator = Translator()
        self._kanglish = KanglishNormalizer()

    async def translate(self, text: str, source_lang: str = "auto",
                         target_lang: str = "en", model: str = None) -> Dict:
        return self._translator.translate(text, source_lang, target_lang)

    async def kanglish_normalize(self, text: str, target: str = "english") -> Dict:
        return self._kanglish.normalize(text, target)

    def get_config(self) -> Dict:
        return {
            "engine": "dictionary",
            "supported_pairs": ["en-kn", "kn-en"],
            "kanglish_support": True,
        }
