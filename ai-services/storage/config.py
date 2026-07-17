STORAGE_CONFIG = {
    "db": {
        "provider": "sqlite",
        "path": "data/ai_memory.db",
    },
    "graph": {
        "provider": "networkx",
    },
    "vector": {
        "provider": "local",
        "model": "all-MiniLM-L6-v2",
        "dimension": 384,
    },
    "cache": {
        "provider": "memory",
        "max_size": 10000,
        "default_ttl": 3600,
    },
    "storage": {
        "provider": "file",
        "base_path": "data/files",
    },
}
