"""Catalyst File Store provider for uploads/attachments/evidence."""

from __future__ import annotations

from typing import List, Optional

from app.db.providers.catalyst_client import CatalystClient
from app.db.providers.catalyst_env import DEFAULT_FILE_FOLDER, cm_getenv
from app.storage.base import StorageProvider
from catalyst_datastore.schema.phase1_tables import FILE_STORE_FOLDER


class CatalystFileProvider(StorageProvider):
    def __init__(self, client: Optional[CatalystClient] = None, folder_name: str = FILE_STORE_FOLDER):
        self.client = client or CatalystClient()
        self.folder_name = (
            folder_name or cm_getenv("CM_FILE_FOLDER", DEFAULT_FILE_FOLDER) or DEFAULT_FILE_FOLDER
        )
        self.folder_id: Optional[str] = cm_getenv("CM_FILE_FOLDER_ID")
        self._index: dict[str, dict] = {}

    async def connect(self) -> None:
        if self.folder_id:
            return
        folders = self.client.list_folders()
        for f in folders or []:
            name = f.get("folder_name") or f.get("name")
            if name == self.folder_name:
                self.folder_id = str(f.get("id") or f.get("folder_id"))
                return
        created = self.client.create_folder(self.folder_name)
        self.folder_id = str(created.get("id") or created.get("folder_id"))

    async def put(self, path: str, data: bytes) -> str:
        await self.connect()
        filename = path.replace("\\", "/").split("/")[-1]
        meta = self.client.upload_file(self.folder_id, filename, data)
        file_id = str(meta.get("id") or meta.get("file_id"))
        self._index[path] = {
            "file_id": file_id,
            "folder_id": self.folder_id,
            "filename": filename,
            "size": len(data),
        }
        # Return a stable logical path that embeds ids for later download/metadata
        return f"catalyst://{self.folder_id}/{file_id}/{filename}"

    def _parse_path(self, path: str) -> tuple[Optional[str], Optional[str]]:
        """Parse catalyst://folder_id/file_id/filename or bare file_id."""
        if path in self._index:
            info = self._index[path]
            return str(info.get("folder_id") or self.folder_id), str(info.get("file_id"))
        if path.startswith("catalyst://"):
            parts = path[len("catalyst://") :].split("/")
            if len(parts) >= 2:
                return parts[0], parts[1]
        # Bare id probe (validator): treat as file_id under configured folder
        if path.isdigit() and self.folder_id:
            return self.folder_id, path
        return self.folder_id, None

    async def get(self, path: str) -> bytes:
        await self.connect()
        folder_id, file_id = self._parse_path(path)
        if not folder_id or not file_id:
            raise FileNotFoundError(f"Cannot resolve Catalyst file path: {path}")
        try:
            return self.client.download_file(folder_id, file_id)
        except Exception as e:
            raise FileNotFoundError(str(e)) from e

    async def delete(self, path: str) -> bool:
        # Soft-delete not implemented; return False to signal no-op
        return False

    async def exists(self, path: str) -> bool:
        return path in self._index or path.startswith("catalyst://") or path.isdigit()

    async def list(self, prefix: str = "") -> List[str]:
        return [p for p in self._index if p.startswith(prefix)]

    async def url(self, path: str) -> str:
        return path

    def last_upload_meta(self, path: str) -> Optional[dict]:
        return self._index.get(path)
