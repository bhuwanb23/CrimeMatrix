import json
import httpx
from typing import Dict, Optional
import structlog

logger = structlog.get_logger()

GOOGLE_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"


class GoogleTranslateClient:
    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=10.0)
        return self._client

    async def translate(self, text: str, src: str = "auto", dest: str = "en") -> Dict:
        try:
            client = self._get_client()
            params = {
                "client": "gtx",
                "sl": src,
                "tl": dest,
                "dt": "t",
                "q": text,
            }
            resp = await client.get(GOOGLE_TRANSLATE_URL, params=params)
            resp.raise_for_status()
            data = resp.json()

            translated = ""
            if data and isinstance(data[0], list):
                translated = "".join(part[0] for part in data[0] if part[0])

            detected_src = data[1] if len(data) > 1 and data[1] else src

            return {
                "original": text,
                "translated": translated,
                "source": detected_src,
                "target": dest,
                "engine": "google",
            }
        except Exception as e:
            logger.warning("google_translate_error", error=str(e))
            return {
                "original": text,
                "translated": text,
                "source": src,
                "target": dest,
                "engine": "google_error",
                "error": str(e),
            }

    async def detect(self, text: str) -> str:
        result = await self.translate(text, dest="en")
        return result.get("source", "en")

    async def close(self):
        if self._client:
            await self._client.aclose()
