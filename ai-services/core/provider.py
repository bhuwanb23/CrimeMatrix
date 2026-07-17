from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Optional, Any
import structlog

logger = structlog.get_logger()


class ModelProvider(ABC):
    """Abstract base for all LLM providers."""

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    async def chat(self, messages: list, model: str = None, **kwargs) -> str:
        pass

    @abstractmethod
    async def stream(self, messages: list, model: str = None, **kwargs) -> AsyncGenerator[str, None]:
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        pass

    @abstractmethod
    async def list_models(self) -> list:
        pass

    def get_token_count(self, text: str) -> int:
        return len(text) // 4


class ProviderRegistry:
    """Global registry of LLM providers."""

    def __init__(self):
        self._providers: Dict[str, ModelProvider] = {}
        self._default: str = None

    def register(self, provider: ModelProvider, default: bool = False):
        name = provider.get_name()
        self._providers[name] = provider
        if default or not self._default:
            self._default = name
        logger.info("provider_registered", name=name, default=default)

    def get(self, name: str = None) -> ModelProvider:
        name = name or self._default
        provider = self._providers.get(name)
        if not provider:
            raise ValueError(f"Provider '{name}' not found. Available: {list(self._providers.keys())}")
        return provider

    def list_all(self) -> list:
        return [
            {"name": p.get_name(), "default": p.get_name() == self._default}
            for p in self._providers.values()
        ]

    @property
    def default_name(self) -> str:
        return self._default


# Global registry
registry = ProviderRegistry()
