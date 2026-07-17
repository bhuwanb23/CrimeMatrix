import os
from typing import List, Optional
from app.storage.local_provider import LocalFileProvider
import structlog

logger = structlog.get_logger()


class StorageService:
    def __init__(self, base_path: str = "data/files"):
        self.provider = LocalFileProvider(base_path)

    async def initialize(self):
        await self.provider.connect()
        logger.info("storage_service_initialized", path=self.provider.base_path)

    async def upload(self, filename: str, data: bytes, folder: str = "uploads") -> Dict:
        path = f"{folder}/{filename}"
        saved_path = await self.provider.put(path, data)
        return {
            "filename": filename,
            "path": saved_path,
            "size": len(data),
            "url": await self.provider.url(saved_path),
        }

    async def download(self, path: str) -> bytes:
        return await self.provider.get(path)

    async def delete(self, path: str) -> bool:
        return await self.provider.delete(path)

    async def exists(self, path: str) -> bool:
        return await self.provider.exists(path)

    async def list_files(self, folder: str = "uploads") -> List[str]:
        return await self.provider.list(folder)

    async def get_url(self, path: str) -> str:
        return await self.provider.url(path)


from typing import Dict
