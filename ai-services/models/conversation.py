from typing import List, Dict, Optional, AsyncGenerator
from core.provider import registry as provider_registry
from models.registry import model_registry
import structlog

logger = structlog.get_logger()


class ConversationModel:
    def __init__(self):
        self._default_provider = "ollama"
        self._default_model = "llama3.2:1b"

    async def chat(self, messages: List[Dict], provider: str = None,
                   model: str = None, **kwargs) -> str:
        provider_name = provider or model_registry.get_provider("conversation") or self._default_provider
        model_name = model or model_registry.get_model_name("conversation") or self._default_model

        try:
            p = provider_registry.get(provider_name)
            return await p.chat(messages, model=model_name, **kwargs)
        except Exception as e:
            logger.error("conversation_chat_error", provider=provider_name, error=str(e))
            raise

    async def stream(self, messages: List[Dict], provider: str = None,
                     model: str = None, **kwargs) -> AsyncGenerator[str, None]:
        provider_name = provider or model_registry.get_provider("conversation") or self._default_provider
        model_name = model or model_registry.get_model_name("conversation") or self._default_model

        try:
            p = provider_registry.get(provider_name)
            async for chunk in p.stream(messages, model=model_name, **kwargs):
                yield chunk
        except Exception as e:
            logger.error("conversation_stream_error", provider=provider_name, error=str(e))
            raise

    def get_config(self) -> Dict:
        return {
            "provider": model_registry.get_provider("conversation") or self._default_provider,
            "model": model_registry.get_model_name("conversation") or self._default_model,
        }
