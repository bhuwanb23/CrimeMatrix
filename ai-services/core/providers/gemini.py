import json
import httpx
from typing import AsyncGenerator
from core.provider import ModelProvider
import structlog

logger = structlog.get_logger()


class GeminiProvider(ModelProvider):
    def __init__(self, api_key: str = "", default_model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.default_model = default_model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    def get_name(self) -> str:
        return "gemini"

    async def chat(self, messages: list, model: str = None, **kwargs) -> str:
        model = model or self.default_model
        if not self.api_key:
            raise ValueError("Gemini API key not configured")

        contents = []
        for msg in messages:
            role = "user" if msg["role"] in ("user", "system") else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/models/{model}:generateContent?key={self.api_key}",
                    json={"contents": contents},
                    timeout=60.0,
                )
                response.raise_for_status()
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            logger.error("gemini_chat_error", error=str(e), model=model)
            raise

    async def stream(self, messages: list, model: str = None, **kwargs) -> AsyncGenerator[str, None]:
        model = model or self.default_model
        if not self.api_key:
            raise ValueError("Gemini API key not configured")

        contents = []
        for msg in messages:
            role = "user" if msg["role"] in ("user", "system") else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})

        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/models/{model}:streamGenerateContent?key={self.api_key}",
                    json={"contents": contents},
                    timeout=60.0,
                ) as response:
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data = json.loads(line[6:])
                            if "candidates" in data:
                                parts = data["candidates"][0]["content"]["parts"]
                                for part in parts:
                                    if "text" in part:
                                        yield part["text"]
        except Exception as e:
            logger.error("gemini_stream_error", error=str(e), model=model)
            raise

    async def health_check(self) -> bool:
        return bool(self.api_key)

    async def list_models(self) -> list:
        if not self.api_key:
            return []
        return [{"name": "gemini-2.0-flash"}, {"name": "gemini-2.0-pro"}]
