import pytest
import asyncio
import os
from storage.sqlite_provider import SQLiteProvider
from storage.networkx_provider import NetworkXProvider
from storage.vector_provider import VectorProvider
from storage.cache_provider import CacheProvider
from storage.file_provider import FileProvider


class TestSQLiteProvider:
    @pytest.mark.asyncio
    async def test_connect_and_create(self):
        db = SQLiteProvider(":memory:")
        await db.connect()
        await db.create_table("test", {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "value": "INTEGER"})
        result = await db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test'")
        assert len(result) > 0
        await db.disconnect()

    @pytest.mark.asyncio
    async def test_insert_and_get(self):
        db = SQLiteProvider(":memory:")
        await db.connect()
        await db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
        row_id = await db.insert("users", {"name": "John"})
        assert row_id == 1
        user = await db.get("users", 1)
        assert user["name"] == "John"
        await db.disconnect()

    @pytest.mark.asyncio
    async def test_query(self):
        db = SQLiteProvider(":memory:")
        await db.connect()
        await db.create_table("items", {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "value": "INTEGER"})
        await db.insert("items", {"name": "a", "value": 10})
        await db.insert("items", {"name": "b", "value": 20})
        rows = await db.query("items")
        assert len(rows) == 2
        rows_filtered = await db.query("items", {"value": 20})
        assert len(rows_filtered) == 1
        await db.disconnect()

    @pytest.mark.asyncio
    async def test_update(self):
        db = SQLiteProvider(":memory:")
        await db.connect()
        await db.create_table("items", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
        await db.insert("items", {"name": "old"})
        updated = await db.update("items", 1, {"name": "new"})
        assert updated is True
        item = await db.get("items", 1)
        assert item["name"] == "new"
        await db.disconnect()

    @pytest.mark.asyncio
    async def test_delete(self):
        db = SQLiteProvider(":memory:")
        await db.connect()
        await db.create_table("items", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
        await db.insert("items", {"name": "delete_me"})
        deleted = await db.delete("items", 1)
        assert deleted is True
        item = await db.get("items", 1)
        assert item is None
        await db.disconnect()

    @pytest.mark.asyncio
    async def test_count(self):
        db = SQLiteProvider(":memory:")
        await db.connect()
        await db.create_table("items", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
        await db.insert("items", {"name": "a"})
        await db.insert("items", {"name": "b"})
        count = await db.count("items")
        assert count == 2
        await db.disconnect()


class TestNetworkXProvider:
    @pytest.mark.asyncio
    async def test_add_node(self):
        g = NetworkXProvider()
        await g.add_node("n1", "person", name="John")
        node = await g.get_node("n1")
        assert node["name"] == "John"
        assert node["type"] == "person"

    @pytest.mark.asyncio
    async def test_add_edge(self):
        g = NetworkXProvider()
        await g.add_node("n1", "person")
        await g.add_node("n2", "crime")
        await g.add_edge("n1", "n2", "involved_in")
        neighbors = await g.get_neighbors("n1")
        assert len(neighbors) == 1
        assert neighbors[0]["id"] == "n2"

    @pytest.mark.asyncio
    async def test_shortest_path(self):
        g = NetworkXProvider()
        await g.add_node("a")
        await g.add_node("b")
        await g.add_node("c")
        await g.add_edge("a", "b")
        await g.add_edge("b", "c")
        path = await g.shortest_path("a", "c")
        assert path == ["a", "b", "c"]

    @pytest.mark.asyncio
    async def test_traverse(self):
        g = NetworkXProvider()
        await g.add_node("a")
        await g.add_node("b")
        await g.add_node("c")
        await g.add_edge("a", "b")
        await g.add_edge("b", "c")
        result = await g.traverse("a", "bfs", 2)
        assert len(result) == 3

    @pytest.mark.asyncio
    async def test_stats(self):
        g = NetworkXProvider()
        await g.add_node("a")
        await g.add_node("b")
        await g.add_edge("a", "b")
        stats = await g.stats()
        assert stats["nodes"] == 2
        assert stats["edges"] == 1

    @pytest.mark.asyncio
    async def test_remove(self):
        g = NetworkXProvider()
        await g.add_node("a")
        assert await g.remove_node("a") is True
        assert await g.get_node("a") is None


class TestVectorProvider:
    @pytest.mark.asyncio
    async def test_add_and_search(self):
        vp = VectorProvider()
        await vp.add("test", "v1", [1.0, 0.0, 0.0], {"name": "first"})
        await vp.add("test", "v2", [0.9, 0.1, 0.0], {"name": "second"})
        await vp.add("test", "v3", [0.0, 0.0, 1.0], {"name": "third"})
        results = await vp.search("test", [1.0, 0.0, 0.0], top_k=2)
        assert results[0]["id"] == "v1"

    @pytest.mark.asyncio
    async def test_get(self):
        vp = VectorProvider()
        await vp.add("test", "v1", [0.1, 0.2], {"name": "test"})
        item = await vp.get("test", "v1")
        assert item["name"] == "test"

    @pytest.mark.asyncio
    async def test_count(self):
        vp = VectorProvider()
        await vp.add("test", "v1", [0.1])
        await vp.add("test", "v2", [0.2])
        assert await vp.count("test") == 2

    @pytest.mark.asyncio
    async def test_delete(self):
        vp = VectorProvider()
        await vp.add("test", "v1", [0.1])
        assert await vp.delete("test", "v1") is True
        assert await vp.get("test", "v1") is None


class TestCacheProvider:
    @pytest.mark.asyncio
    async def test_set_get(self):
        cache = CacheProvider()
        await cache.set("key1", "value1", 60)
        val = await cache.get("key1")
        assert val == "value1"

    @pytest.mark.asyncio
    async def test_expiry(self):
        cache = CacheProvider()
        await cache.set("key1", "value1", 0)
        val = await cache.get("key1")
        assert val is None

    @pytest.mark.asyncio
    async def test_delete(self):
        cache = CacheProvider()
        await cache.set("key1", "value1", 60)
        assert await cache.delete("key1") is True
        assert await cache.get("key1") is None

    @pytest.mark.asyncio
    async def test_exists(self):
        cache = CacheProvider()
        await cache.set("key1", "value1", 60)
        assert await cache.exists("key1") is True
        assert await cache.exists("missing") is False

    @pytest.mark.asyncio
    async def test_clear(self):
        cache = CacheProvider()
        await cache.set("a", 1, 60)
        await cache.set("b", 2, 60)
        await cache.clear()
        assert await cache.exists("a") is False


class TestFileProvider:
    @pytest.mark.asyncio
    async def test_put_and_get(self):
        fp = FileProvider("test_files")
        await fp.connect()
        await fp.put("test.txt", b"hello world")
        data = await fp.get("test.txt")
        assert data == b"hello world"
        await fp.delete("test.txt")

    @pytest.mark.asyncio
    async def test_exists(self):
        fp = FileProvider("test_files")
        await fp.connect()
        await fp.put("exists.txt", b"data")
        assert await fp.exists("exists.txt") is True
        assert await fp.exists("nope.txt") is False
        await fp.delete("exists.txt")

    @pytest.mark.asyncio
    async def test_list(self):
        fp = FileProvider("test_files")
        await fp.connect()
        await fp.put("a.txt", b"a")
        await fp.put("b.txt", b"b")
        files = await fp.list()
        assert len(files) >= 2
        await fp.delete("a.txt")
        await fp.delete("b.txt")
