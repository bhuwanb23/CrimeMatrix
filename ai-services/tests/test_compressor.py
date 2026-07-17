import pytest
from memory.compressor import ContextCompressor


class TestContextCompressor:
    @pytest.mark.asyncio
    async def test_compress_few_messages(self):
        comp = ContextCompressor()
        messages = [{"role": "user", "content": "hi"}]
        summary, kept = await comp.compress(messages)
        assert summary == ""
        assert kept == messages

    @pytest.mark.asyncio
    async def test_compress_empty(self):
        comp = ContextCompressor()
        summary, kept = await comp.compress([])
        assert summary == ""
        assert kept == []
