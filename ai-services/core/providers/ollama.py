import json
import httpx
from typing import AsyncGenerator, List, Dict
from core.provider import ModelProvider
import structlog

logger = structlog.get_logger()


class OllamaProvider(ModelProvider):
    def __init__(self, base_url: str = "http://localhost:11434", default_model: str = "llama3.2:1b"):
        self.base_url = base_url
        self.default_model = default_model

    def get_name(self) -> str:
        return "ollama"

    async def chat(self, messages: list, model: str = None, **kwargs) -> str:
        model = model or self.default_model
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json={"model": model, "messages": messages, "stream": False},
                    timeout=120.0,
                )
                response.raise_for_status()
                return response.json()["message"]["content"]
        except Exception as e:
            logger.error("ollama_chat_error", error=str(e), model=model)
            raise

    async def stream(self, messages: list, model: str = None, **kwargs) -> AsyncGenerator[str, None]:
        model = model or self.default_model
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/chat",
                    json={"model": model, "messages": messages, "stream": True},
                    timeout=120.0,
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            data = json.loads(line)
                            if "message" in data and "content" in data["message"]:
                                yield data["message"]["content"]
        except Exception as e:
            logger.error("ollama_stream_error", error=str(e), model=model)
            raise

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags", timeout=5.0)
                return response.status_code == 200
        except Exception:
            return False

    async def list_models(self) -> list:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags", timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    return [{"name": m["name"], "size": m.get("size", 0)} for m in data.get("models", [])]
            return []
        except Exception:
            return []
