import pytest
from memory.manager import MemoryManager


class TestMemoryManager:
    @pytest.mark.asyncio
    async def test_get_session(self):
        mm = MemoryManager()
        s = await mm.get_session("test1")
        assert s.session_id == "test1"

    @pytest.mark.asyncio
    async def test_session_persistence(self):
        mm = MemoryManager()
        s1 = await mm.get_session("test1")
        s2 = await mm.get_session("test1")
        assert s1 is s2

    @pytest.mark.asyncio
    async def test_clear_session(self):
        mm = MemoryManager()
        await mm.get_session("test1")
        assert await mm.clear_session("test1") is True
        assert await mm.clear_session("test1") is True

    @pytest.mark.asyncio
    async def test_list_sessions(self):
        mm = MemoryManager()
        await mm.get_session("s1")
        await mm.get_session("s2")
        sessions = await mm.list_sessions()
        assert len(sessions) >= 1

    @pytest.mark.asyncio
    async def test_before_turn(self):
        mm = MemoryManager()
        ctx = await mm.before_turn("Hello", "s1", "u1")
        assert "conversation_context" in ctx
        assert "preferences" in ctx

    @pytest.mark.asyncio
    async def test_after_turn(self):
        mm = MemoryManager()
        uid = "after_turn_%s" % id(mm)
        await mm.after_turn("Hello", "Hi there", uid)
        session = await mm.get_session(uid)
        assert len(session.messages) == 2
        assert session.messages[0]["content"] == "Hello"
        assert session.messages[1]["content"] == "Hi there"

    @pytest.mark.asyncio
    async def test_multi_turn(self):
        mm = MemoryManager()
        uid = "multi_turn_%s" % id(mm)
        await mm.after_turn("What crimes are there?", "There are theft cases", uid)
        await mm.after_turn("Tell me about the first one", "The first one is...", uid)
        session = await mm.get_session(uid)
        assert len(session.messages) == 4

    @pytest.mark.asyncio
    async def test_working_memory(self):
        mm = MemoryManager()
        mm.working.set("result", 42)
        ctx = await mm.before_turn("next query", "s1", "u1")
        assert "42" in ctx["conversation_context"]

    def test_preferences(self):
        mm = MemoryManager()
        mm.preferences.set("u1", "language", "hi")
        prefs = mm.preferences.get("u1")
        assert prefs["language"] == "hi"
