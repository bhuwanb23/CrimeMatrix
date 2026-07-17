import time
from typing import Any, Dict, List, Optional
from storage.base import CacheProvider
import structlog

logger = structlog.get_logger()


class CacheProvider(CacheProvider):
    def __init__(self, max_size: int = 10000):
        self._store: Dict[str, Dict] = {}
        self._max_size = max_size

    async def connect(self):
        logger.info("cache_provider_connected", max_size=self._max_size)

    async def disconnect(self):
        pass

    async def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if not entry:
            return None
        if entry.get("expires_at") and time.time() > entry["expires_at"]:
            del self._store[key]
            return None
        return entry["value"]

    async def set(self, key: str, value: Any, ttl_seconds: int = 3600):
        if len(self._store) >= self._max_size:
            self._evict()
        self._store[key] = {
            "value": value,
            "created_at": time.time(),
            "expires_at": time.time() - 1 if ttl_seconds == 0 else (time.time() + ttl_seconds if ttl_seconds > 0 else None),
        }

    async def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False

    async def exists(self, key: str) -> bool:
        entry = self._store.get(key)
        if not entry:
            return False
        if entry.get("expires_at") and time.time() > entry["expires_at"]:
            del self._store[key]
            return False
        return True

    async def keys(self, pattern: str = "*") -> List[str]:
        if pattern == "*":
            return list(self._store.keys())
        import fnmatch
        return [k for k in self._store if fnmatch.fnmatch(k, pattern)]

    async def clear(self):
        self._store.clear()

    async def ttl(self, key: str) -> int:
        entry = self._store.get(key)
        if not entry or not entry.get("expires_at"):
            return -1
        remaining = int(entry["expires_at"] - time.time())
        return max(0, remaining)

    def _evict(self):
        if self._store:
            oldest_key = min(self._store.keys(), key=lambda k: self._store[k].get("created_at", 0))
            del self._store[oldest_key]
