from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class DBProvider(ABC):
    @abstractmethod
    async def connect(self): pass

    @abstractmethod
    async def disconnect(self): pass

    @abstractmethod
    async def create_table(self, table_name: str, schema: Dict[str, str]): pass

    @abstractmethod
    async def insert(self, table: str, data: Dict) -> Any: pass

    @abstractmethod
    async def get(self, table: str, record_id: Any) -> Optional[Dict]: pass

    @abstractmethod
    async def query(self, table: str, filters: Dict = None, limit: int = 100, offset: int = 0) -> List[Dict]: pass

    @abstractmethod
    async def update(self, table: str, record_id: Any, data: Dict) -> bool: pass

    @abstractmethod
    async def delete(self, table: str, record_id: Any) -> bool: pass

    @abstractmethod
    async def count(self, table: str, filters: Dict = None) -> int: pass

    @abstractmethod
    async def execute(self, sql: str, params: tuple = ()) -> List[Dict]: pass


class GraphProvider(ABC):
    @abstractmethod
    async def add_node(self, node_id: str, node_type: str = "", **attrs): pass

    @abstractmethod
    async def add_edge(self, source: str, target: str, relation: str = "", **attrs): pass

    @abstractmethod
    async def get_node(self, node_id: str) -> Optional[Dict]: pass

    @abstractmethod
    async def get_neighbors(self, node_id: str, edge_type: str = None) -> List[Dict]: pass

    @abstractmethod
    async def shortest_path(self, source: str, target: str) -> List[str]: pass

    @abstractmethod
    async def traverse(self, start: str, method: str = "bfs", max_depth: int = 5) -> List[Dict]: pass

    @abstractmethod
    async def get_nodes(self, node_type: str = None) -> List[Dict]: pass

    @abstractmethod
    async def get_edges(self) -> List[Dict]: pass

    @abstractmethod
    async def remove_node(self, node_id: str) -> bool: pass

    @abstractmethod
    async def remove_edge(self, source: str, target: str) -> bool: pass

    @abstractmethod
    async def stats(self) -> Dict: pass

    @abstractmethod
    async def clear(self): pass


class VectorProvider(ABC):
    @abstractmethod
    async def add(self, collection: str, item_id: str, vector: list, metadata: dict = None): pass

    @abstractmethod
    async def search(self, collection: str, query_vector: list, top_k: int = 5) -> List[Dict]: pass

    @abstractmethod
    async def get(self, collection: str, item_id: str) -> Optional[Dict]: pass

    @abstractmethod
    async def delete(self, collection: str, item_id: str) -> bool: pass

    @abstractmethod
    async def count(self, collection: str) -> int: pass

    @abstractmethod
    async def list_collections(self) -> List[str]: pass

    @abstractmethod
    async def clear(self, collection: str): pass


class CacheProvider(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]: pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl_seconds: int = 3600): pass

    @abstractmethod
    async def delete(self, key: str) -> bool: pass

    @abstractmethod
    async def exists(self, key: str) -> bool: pass

    @abstractmethod
    async def keys(self, pattern: str = "*") -> List[str]: pass

    @abstractmethod
    async def clear(self): pass

    @abstractmethod
    async def ttl(self, key: str) -> int: pass


class StorageProvider(ABC):
    @abstractmethod
    async def put(self, path: str, data: bytes) -> str: pass

    @abstractmethod
    async def get(self, path: str) -> bytes: pass

    @abstractmethod
    async def delete(self, path: str) -> bool: pass

    @abstractmethod
    async def exists(self, path: str) -> bool: pass

    @abstractmethod
    async def list(self, prefix: str = "") -> List[str]: pass

    @abstractmethod
    async def url(self, path: str) -> str: pass
