from .base import AIProvider
from typing import AsyncGenerator
import httpx
import structlog

logger = structlog.get_logger()


class OllamaProvider(AIProvider):
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    async def chat(self, message: str, context: dict = None) -> str:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json={
                        "model": "llama3.2",
                        "messages": [{"role": "user", "content": message}],
                        "stream": False,
                    },
                    timeout=60.0,
                )
                response.raise_for_status()
                return response.json()["message"]["content"]
        except Exception as e:
            logger.error("ollama_chat_error", error=str(e))
            raise

    async def stream(self, message: str, context: dict = None) -> AsyncGenerator[str, None]:
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/chat",
                    json={
                        "model": "llama3.2",
                        "messages": [{"role": "user", "content": message}],
                        "stream": True,
                    },
                    timeout=60.0,
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            import json
                            data = json.loads(line)
                            if "message" in data and "content" in data["message"]:
                                yield data["message"]["content"]
        except Exception as e:
            logger.error("ollama_stream_error", error=str(e))
            raise

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags", timeout=5.0)
                return response.status_code == 200
        except Exception:
            return False
