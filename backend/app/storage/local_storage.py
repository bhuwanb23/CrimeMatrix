import os
import shutil
from typing import Optional
import structlog

logger = structlog.get_logger()

STORAGE_DIR = "data/uploads"


class LocalStorage:
    def __init__(self):
        os.makedirs(STORAGE_DIR, exist_ok=True)

    def _get_path(self, filename: str) -> str:
        return os.path.join(STORAGE_DIR, filename)

    async def upload(self, filename: str, data: bytes) -> str:
        path = self._get_path(filename)
        with open(path, "wb") as f:
            f.write(data)
        logger.info("file_uploaded", filename=filename, size=len(data))
        return path

    async def download(self, filename: str) -> Optional[bytes]:
        path = self._get_path(filename)
        if not os.path.exists(path):
            return None
        with open(path, "rb") as f:
            return f.read()

    async def delete(self, filename: str) -> bool:
        path = self._get_path(filename)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    async def list_files(self) -> list:
        return os.listdir(STORAGE_DIR)

    async def get_url(self, filename: str) -> str:
        return f"/api/v1/files/{filename}"
