from typing import Dict
import structlog

logger = structlog.get_logger()


class TextToSpeech:
    def __init__(self):
        self._voices = {
            "en": {"male": "en-US-Guy", "female": "en-US-Jenny"},
            "kn": {"male": "kn-IN-Gagan", "female": "kn-IN-Sapna"},
            "hi": {"male": "hi-IN-Madhur", "female": "hi-IN-Swara"},
        }

    async def synthesize(self, text: str, voice: str = "default",
                          language: str = "en", gender: str = "female") -> Dict:
        lang = language if language in self._voices else "en"
        voice_id = self._voices.get(lang, {}).get(gender, "en-US-Jenny")

        ssml = self._generate_ssml(text, voice_id, lang)

        return {
            "ssml": ssml,
            "text": text,
            "voice": voice_id,
            "language": lang,
            "gender": gender,
            "format": "ssml",
            "note": "SSML output ready for TTS engine (Azure, Google, etc.)",
        }

    def _generate_ssml(self, text: str, voice: str, lang: str) -> str:
        lang_code = {"en": "en-US", "kn": "kn-IN", "hi": "hi-IN"}.get(lang, "en-US")
        return f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{lang_code}">
  <voice name="{voice}">
    <prosody rate="medium" pitch="medium">
      {text}
    </prosody>
  </voice>
</speak>"""

    def get_voices(self) -> Dict:
        return self._voices
