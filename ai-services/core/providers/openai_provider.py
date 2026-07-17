import json
import httpx
from typing import AsyncGenerator
from core.provider import ModelProvider
import structlog

logger = structlog.get_logger()


class OpenAIProvider(ModelProvider):
    def __init__(self, api_key: str = "", base_url: str = "https://api.openai.com/v1",
                 default_model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.base_url = base_url
        self.default_model = default_model

    def get_name(self) -> str:
        return "openai"

    async def chat(self, messages: list, model: str = None, **kwargs) -> str:
        model = model or self.default_model
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={"model": model, "messages": messages, "stream": False},
                    timeout=60.0,
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error("openai_chat_error", error=str(e), model=model)
            raise

    async def stream(self, messages: list, model: str = None, **kwargs) -> AsyncGenerator[str, None]:
        model = model or self.default_model
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={"model": model, "messages": messages, "stream": True},
                    timeout=60.0,
                ) as response:
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data = line[6:]
                            if data.strip() == "[DONE]":
                                break
                            chunk = json.loads(data)
                            delta = chunk["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
        except Exception as e:
            logger.error("openai_stream_error", error=str(e), model=model)
            raise

    async def health_check(self) -> bool:
        if not self.api_key:
            return False
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=5.0,
                )
                return response.status_code == 200
        except Exception:
            return False

    async def list_models(self) -> list:
        if not self.api_key:
            return []
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=5.0,
                )
                if response.status_code == 200:
                    data = response.json()
                    return [{"name": m["id"]} for m in data.get("data", [])]
            return []
        except Exception:
            return []
