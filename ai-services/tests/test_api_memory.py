import pytest
from unittest.mock import patch, AsyncMock


class TestAPIHealth:
    @pytest.mark.asyncio
    async def test_health_endpoint(self):
        from httpx import AsyncClient, ASGITransport
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/api/ai/health")
            assert resp.status_code == 200
            data = resp.json()
            assert data["success"] is True
            assert "providers" in data["data"]


class TestAPITools:
    @pytest.mark.asyncio
    async def test_list_tools(self):
        from httpx import AsyncClient, ASGITransport
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/api/ai/tools")
            assert resp.status_code == 200
            data = resp.json()
            assert data["success"] is True
            assert len(data["data"]) >= 2

    @pytest.mark.asyncio
    async def test_calculator_tool(self):
        from httpx import AsyncClient, ASGITransport
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post("/api/ai/tools/invoke", json={"tool": "calculator", "params": {"expression": "10 + 5"}})
            assert resp.status_code == 200
            assert "15" in resp.json()["data"]["result"]


class TestAPIMemory:
    @pytest.mark.asyncio
    async def test_preferences(self):
        from httpx import AsyncClient, ASGITransport
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.put("/api/ai/memory/preferences/test_user", json={"key": "language", "value": "hi"})
            assert resp.status_code == 200
            resp2 = await client.get("/api/ai/memory/preferences/test_user")
            assert resp2.json()["data"]["language"] == "hi"

    @pytest.mark.asyncio
    async def test_working_memory(self):
        from httpx import AsyncClient, ASGITransport
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/api/ai/memory/working")
            assert resp.status_code == 200
            assert resp.json()["success"] is True


class TestAPISessions:
    @pytest.mark.asyncio
    async def test_sessions_list(self):
        from httpx import AsyncClient, ASGITransport
        from main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/api/ai/sessions")
            assert resp.status_code == 200
            assert resp.json()["success"] is True
