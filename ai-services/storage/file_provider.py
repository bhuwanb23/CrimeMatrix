import os
import uuid
from typing import List
from storage.base import StorageProvider
import structlog

logger = structlog.get_logger()


class FileProvider(StorageProvider):
    def __init__(self, base_path: str = "data/files"):
        self.base_path = base_path

    async def connect(self):
        os.makedirs(self.base_path, exist_ok=True)
        logger.info("file_provider_connected", path=self.base_path)

    async def disconnect(self):
        pass

    async def put(self, path: str, data: bytes) -> str:
        full_path = os.path.join(self.base_path, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "wb") as f:
            f.write(data)
        return path

    async def get(self, path: str) -> bytes:
        full_path = os.path.join(self.base_path, path)
        with open(full_path, "rb") as f:
            return f.read()

    async def delete(self, path: str) -> bool:
        full_path = os.path.join(self.base_path, path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False

    async def exists(self, path: str) -> bool:
        full_path = os.path.join(self.base_path, path)
        return os.path.exists(full_path)

    async def list(self, prefix: str = "") -> List[str]:
        results = []
        full_prefix = os.path.join(self.base_path, prefix)
        for root, dirs, files in os.walk(full_prefix):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, self.base_path)
                results.append(rel)
        return results

    async def url(self, path: str) -> str:
        return f"file://{os.path.join(self.base_path, path)}"
