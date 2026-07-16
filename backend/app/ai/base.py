from abc import ABC, abstractmethod
from typing import AsyncGenerator


class AIProvider(ABC):
    @abstractmethod
    async def chat(self, message: str, context: dict = None) -> str:
        pass

    @abstractmethod
    async def stream(self, message: str, context: dict = None) -> AsyncGenerator[str, None]:
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        pass
