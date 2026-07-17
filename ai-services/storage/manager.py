from typing import Optional
from storage.config import STORAGE_CONFIG
from storage.sqlite_provider import SQLiteProvider
from storage.networkx_provider import NetworkXProvider
from storage.vector_provider import VectorProvider
from storage.cache_provider import MemoryCacheProvider
from storage.file_provider import FileProvider
import structlog

logger = structlog.get_logger()


class StorageManager:
    def __init__(self, config: dict = None):
        self.config = config or STORAGE_CONFIG
        self.db: Optional[SQLiteProvider] = None
        self.graph: Optional[NetworkXProvider] = None
        self.vector: Optional[VectorProvider] = None
        self.cache: Optional[MemoryCacheProvider] = None
        self.storage: Optional[FileProvider] = None

    async def initialize(self):
        db_cfg = self.config.get("db", {})
        self.db = SQLiteProvider(db_cfg.get("path", "data/ai_memory.db"))
        await self.db.connect()

        self.graph = NetworkXProvider()
        await self.graph.connect()

        self.vector = VectorProvider()
        await self.vector.connect()

        cache_cfg = self.config.get("cache", {})
        self.cache = MemoryCacheProvider(cache_cfg.get("max_size", 10000))
        await self.cache.connect()

        storage_cfg = self.config.get("storage", {})
        self.storage = FileProvider(storage_cfg.get("base_path", "data/files"))
        await self.storage.connect()

        logger.info("storage_initialized", providers=["sqlite", "networkx", "vector", "cache", "file"])

    async def shutdown(self):
        if self.db:
            await self.db.disconnect()
        logger.info("storage_shutdown")


storage = StorageManager()
