from typing import Dict
from models.registry import model_registry
import structlog

logger = structlog.get_logger()


class TranslationModel:
    def __init__(self):
        self._translator = None
        self._fallback_translator = None

    def _get_translator(self):
        if self._translator is None:
            try:
                from googletrans import Translator
                self._translator = Translator()
            except Exception as e:
                logger.warning("googletrans_unavailable", error=str(e))
                self._translator = "fallback"
        return self._translator

    def _get_fallback(self):
        if self._fallback_translator is None:
            from language.translator import Translator
            self._fallback_translator = Translator()
        return self._fallback_translator

    async def translate(self, text: str, source_lang: str = "auto",
                         target_lang: str = "en", model: str = None) -> Dict:
        t = self._get_translator()

        if t == "fallback":
            fb = self._get_fallback()
            return fb.translate(text, source_lang, target_lang)

        lang_map = {"en": "en", "kn": "kn", "hi": "hi"}
        src = lang_map.get(source_lang, "auto")
        tgt = lang_map.get(target_lang, "en")

        try:
            result = t.translate(text, src=src, dest=tgt)
            return {
                "original": text,
                "translated": result.text,
                "source": result.src,
                "target": result.dest,
                "engine": "google",
            }
        except Exception as e:
            logger.warning("google_translate_error", error=str(e))
            fb = self._get_fallback()
            return fb.translate(text, source_lang, target_lang)

    async def kanglish_normalize(self, text: str, target: str = "english") -> Dict:
        from language.kanglish import KanglishNormalizer
        kn = KanglishNormalizer()
        return kn.normalize(text, target)

    def get_config(self) -> Dict:
        t = self._get_translator()
        return {
            "engine": "google" if t != "fallback" else "dictionary",
            "supported_pairs": ["auto-en", "en-kn", "kn-en", "en-hi", "hi-en"],
            "kanglish_support": True,
        }
