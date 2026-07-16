from .base import AIProvider
from typing import AsyncGenerator
import structlog

logger = structlog.get_logger()


class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def chat(self, message: str, context: dict = None) -> str:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.api_key)
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": message}],
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error("openai_chat_error", error=str(e))
            raise

    async def stream(self, message: str, context: dict = None) -> AsyncGenerator[str, None]:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.api_key)
            stream = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": message}],
                stream=True,
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error("openai_stream_error", error=str(e))
            raise

    async def health_check(self) -> bool:
        return bool(self.api_key)
