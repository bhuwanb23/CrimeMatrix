from typing import Dict
from models.registry import model_registry
from models.google_translate import GoogleTranslateClient
import structlog

logger = structlog.get_logger()


class TranslationModel:
    def __init__(self):
        self._google = GoogleTranslateClient()
        self._fallback = None

    def _get_fallback(self):
        if self._fallback is None:
            from language.translator import Translator
            self._fallback = Translator()
        return self._fallback

    async def translate(self, text: str, source_lang: str = "auto",
                         target_lang: str = "en", model: str = None) -> Dict:
        result = await self._google.translate(text, src=source_lang, dest=target_lang)

        if result.get("engine") == "google_error":
            fb = self._get_fallback()
            return fb.translate(text, source_lang, target_lang)

        return result

    async def kanglish_normalize(self, text: str, target: str = "english") -> Dict:
        from language.kanglish import KanglishNormalizer
        kn = KanglishNormalizer()
        return kn.normalize(text, target)

    def get_config(self) -> Dict:
        return {
            "engine": "google_direct",
            "supported_pairs": ["auto-en", "en-kn", "kn-en", "en-hi", "hi-en"],
            "kanglish_support": True,
        }
