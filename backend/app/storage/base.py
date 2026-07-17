from abc import ABC, abstractmethod
from typing import List


class StorageProvider(ABC):
    @abstractmethod
    async def put(self, path: str, data: bytes) -> str:
        pass

    @abstractmethod
    async def get(self, path: str) -> bytes:
        pass

    @abstractmethod
    async def delete(self, path: str) -> bool:
        pass

    @abstractmethod
    async def exists(self, path: str) -> bool:
        pass

    @abstractmethod
    async def list(self, prefix: str = "") -> List[str]:
        pass

    @abstractmethod
    async def url(self, path: str) -> str:
        pass
