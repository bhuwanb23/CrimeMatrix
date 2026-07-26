import os
from typing import Dict, List, Optional
from app.storage.local_provider import LocalFileProvider
import structlog

logger = structlog.get_logger()


def _build_provider(base_path: str = "data/files"):
    kind = (os.getenv("STORAGE_PROVIDER") or os.getenv("DB_PROVIDER") or "local").strip().lower()
    if kind == "catalyst":
        from app.storage.catalyst_provider import CatalystFileProvider

        return CatalystFileProvider()
    return LocalFileProvider(base_path)


class StorageService:
    def __init__(self, base_path: str = "data/files"):
        self.provider = _build_provider(base_path)

    async def initialize(self):
        connect = getattr(self.provider, "connect", None)
        if connect:
            await connect()
        logger.info(
            "storage_service_initialized",
            provider=type(self.provider).__name__,
        )

    async def upload(self, filename: str, data: bytes, folder: str = "uploads") -> Dict:
        path = f"{folder}/{filename}"
        saved_path = await self.provider.put(path, data)
        meta = {"filename": filename, "path": saved_path, "size": len(data), "url": await self.provider.url(saved_path)}
        last = getattr(self.provider, "last_upload_meta", None)
        if last:
            # last_upload_meta expects original path key used in put
            info = last(path) or {}
            if info:
                meta["file_id"] = info.get("file_id")
                meta["folder_id"] = info.get("folder_id")
        return meta

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
