from typing import Any, Optional
import json
import os
import time
import structlog

logger = structlog.get_logger()

CACHE_DIR = "data/cache"


class LocalCache:
    def __init__(self):
        os.makedirs(CACHE_DIR, exist_ok=True)

    def _get_path(self, key: str) -> str:
        safe_key = key.replace("/", "_").replace("\\", "_")
        return os.path.join(CACHE_DIR, f"{safe_key}.json")

    def get(self, key: str) -> Optional[Any]:
        path = self._get_path(key)
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r") as f:
                data = json.load(f)
            if data.get("expires_at") and data["expires_at"] < time.time():
                os.remove(path)
                return None
            return data.get("value")
        except Exception:
            return None

    def set(self, key: str, value: Any, ttl: int = None):
        path = self._get_path(key)
        data = {
            "value": value,
            "created_at": time.time(),
            "expires_at": time.time() + ttl if ttl else None,
        }
        with open(path, "w") as f:
            json.dump(data, f)

    def delete(self, key: str):
        path = self._get_path(key)
        if os.path.exists(path):
            os.remove(path)

    def clear(self):
        for f in os.listdir(CACHE_DIR):
            if f.endswith(".json"):
                os.remove(os.path.join(CACHE_DIR, f))

    def publish(self, channel: str, message: Any):
        logger.info("cache_publish", channel=channel, message=str(message)[:100])

    def subscribe(self, channel: str, callback):
        logger.info("cache_subscribe", channel=channel)
