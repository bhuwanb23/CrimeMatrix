from typing import Dict
import structlog

logger = structlog.get_logger()


class SpeechToText:
    def __init__(self):
        self._supported_formats = ["wav", "mp3", "webm", "ogg", "flac"]

    async def transcribe(self, audio_data: bytes = None, audio_text: str = None,
                          language: str = "auto") -> Dict:
        if audio_text:
            return {
                "text": audio_text,
                "language": self._detect_language(audio_text),
                "confidence": 0.95,
                "engine": "text_input",
                "duration_ms": 0,
            }

        if audio_data:
            return {
                "text": "[Audio transcribed - stub implementation]",
                "language": "en",
                "confidence": 0.0,
                "engine": "stub",
                "duration_ms": 0,
                "note": "Full STT requires external service (Whisper, Google STT)",
            }

        return {"text": "", "language": "unknown", "confidence": 0, "error": "No audio input provided"}

    def _detect_language(self, text: str) -> str:
        kannada_chars = sum(1 for c in text if 0x0C80 <= ord(c) <= 0x0CFF)
        if kannada_chars > len(text) * 0.3:
            return "kn"
        hindi_chars = sum(1 for c in text if 0x0900 <= ord(c) <= 0x097F)
        if hindi_chars > len(text) * 0.3:
            return "hi"
        return "en"

    def get_supported_formats(self) -> list:
        return self._supported_formats
