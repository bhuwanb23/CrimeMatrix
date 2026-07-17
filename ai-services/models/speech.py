from typing import Dict
from language.stt import SpeechToText
from language.tts import TextToSpeech
from models.registry import model_registry
import structlog

logger = structlog.get_logger()


class SpeechModel:
    def __init__(self):
        self._stt = SpeechToText()
        self._tts = TextToSpeech()

    async def transcribe(self, audio_text: str = None, language: str = "auto",
                          model: str = None) -> Dict:
        return await self._stt.transcribe(audio_text=audio_text, language=language)

    async def synthesize(self, text: str, language: str = "en",
                          gender: str = "female", model: str = None) -> Dict:
        return await self._tts.synthesize(text, language=language, gender=gender)

    def get_config(self) -> Dict:
        return {
            "stt_engine": "stub",
            "tts_engine": "ssml",
            "supported_languages": ["en", "kn", "hi"],
        }
