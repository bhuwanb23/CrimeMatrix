from .base import AIProvider
from typing import AsyncGenerator
import structlog

logger = structlog.get_logger()


class GeminiProvider(AIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def chat(self, message: str, context: dict = None) -> str:
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=message,
            )
            return response.text
        except Exception as e:
            logger.error("gemini_chat_error", error=str(e))
            raise

    async def stream(self, message: str, context: dict = None) -> AsyncGenerator[str, None]:
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content_stream(
                model="gemini-2.0-flash",
                contents=message,
            )
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            logger.error("gemini_stream_error", error=str(e))
            raise

    async def health_check(self) -> bool:
        return bool(self.api_key)
