import pytest
from memory.investigation import InvestigationContext


class TestInvestigationContext:
    def test_format_for_context(self):
        ic = InvestigationContext()
        data = {"title": "Murder Case", "status": "open", "id": 1, "created_at": "2024-01-01"}
        result = ic.format_for_context(data, "crime")
        assert "Murder Case" in result
        assert "open" in result
        assert "id" not in result

    def test_format_empty(self):
        ic = InvestigationContext()
        result = ic.format_for_context(None)
        assert "No data" in result

    @pytest.mark.asyncio
    async def test_cache(self):
        ic = InvestigationContext()
        await ic._cache.set("test_key", {"data": "cached"}, 60)
        val = await ic._cache.get("test_key")
        assert val["data"] == "cached"

    @pytest.mark.asyncio
    async def test_clear_cache(self):
        ic = InvestigationContext()
        await ic._cache.set("key", {"data": "val"}, 60)
        await ic.clear_cache()
        val = await ic._cache.get("key")
        assert val is None
