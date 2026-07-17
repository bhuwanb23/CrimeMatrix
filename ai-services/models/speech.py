from typing import Dict
from language.tts import TextToSpeech
from models.registry import model_registry
import structlog

logger = structlog.get_logger()


class SpeechModel:
    def __init__(self):
        self._tts = TextToSpeech()
        self._whisper = None

    def _get_whisper(self):
        if self._whisper is None:
            try:
                import whisper
                self._whisper = whisper.load_model("base")
                logger.info("whisper_model_loaded")
            except Exception as e:
                logger.warning("whisper_unavailable", error=str(e))
                self._whisper = "stub"
        return self._whisper

    async def transcribe(self, audio_text: str = None, audio_path: str = None,
                          language: str = "auto", model: str = None) -> Dict:
        if audio_text:
            return {
                "text": audio_text,
                "language": self._detect_lang(audio_text),
                "confidence": 0.95,
                "engine": "text_input",
            }

        if audio_path:
            whisper_model = self._get_whisper()
            if whisper_model != "stub":
                try:
                    result = whisper_model.transcribe(audio_path)
                    return {
                        "text": result["text"],
                        "language": result.get("language", "unknown"),
                        "confidence": 0.9,
                        "engine": "whisper",
                    }
                except Exception as e:
                    logger.error("whisper_transcribe_error", error=str(e))

        return {"text": "", "language": "unknown", "confidence": 0, "engine": "stub"}

    async def synthesize(self, text: str, language: str = "en",
                          gender: str = "female", model: str = None) -> Dict:
        return await self._tts.synthesize(text, language=language, gender=gender)

    def _detect_lang(self, text: str) -> str:
        kannada = sum(1 for c in text if 0x0C80 <= ord(c) <= 0x0CFF)
        if kannada > len(text) * 0.3:
            return "kn"
        return "en"

    def get_config(self) -> Dict:
        w = self._get_whisper()
        return {
            "stt_engine": "whisper" if w != "stub" else "stub",
            "tts_engine": "ssml",
            "supported_languages": ["en", "kn", "hi"],
        }
