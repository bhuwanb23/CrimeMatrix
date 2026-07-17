import pytest
from memory.session import SessionMemory


class TestSessionMemory:
    def test_add_message(self):
        mem = SessionMemory("test1")
        mem.add_message("user", "Hello")
        mem.add_message("assistant", "Hi there")
        assert len(mem.messages) == 2

    def test_get_messages(self):
        mem = SessionMemory("test1")
        mem.add_message("user", "Hello")
        msgs = mem.get_messages()
        assert len(msgs) == 1
        assert msgs[0]["role"] == "user"
        assert msgs[0]["content"] == "Hello"

    def test_get_context_with_summary(self):
        mem = SessionMemory("test1")
        mem.set_summary("Earlier discussion about crimes", 5)
        mem.add_message("user", "Tell me more")
        ctx = mem.get_context()
        assert any("summary" in m.get("content", "").lower() for m in ctx)

    def test_needs_compression(self):
        mem = SessionMemory("test1", max_messages=5)
        for i in range(6):
            mem.add_message("user", f"msg {i}")
        assert mem.needs_compression() is True

    def test_does_not_need_compression(self):
        mem = SessionMemory("test1", max_messages=10)
        for i in range(5):
            mem.add_message("user", f"msg {i}")
        assert mem.needs_compression() is False

    def test_clear(self):
        mem = SessionMemory("test1")
        mem.add_message("user", "Hello")
        mem.set_summary("summary", 1)
        mem.clear()
        assert len(mem.messages) == 0
        assert mem.summary == ""

    def test_to_dict(self):
        mem = SessionMemory("test1")
        mem.add_message("user", "Hello")
        d = mem.to_dict()
        assert d["session_id"] == "test1"
        assert d["message_count"] == 1

    def test_get_unsummarized_messages(self):
        mem = SessionMemory("test1")
        for i in range(10):
            mem.add_message("user", f"msg {i}")
        mem.set_summary("old stuff", 5)
        unsummarized = mem.get_unsummarized_messages()
        assert len(unsummarized) == 5
