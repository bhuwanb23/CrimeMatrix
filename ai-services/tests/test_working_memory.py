import pytest
from memory.working import WorkingMemory


class TestWorkingMemory:
    def test_set_and_get(self):
        wm = WorkingMemory()
        wm.set("key1", "value1")
        assert wm.get("key1") == "value1"

    def test_get_default(self):
        wm = WorkingMemory()
        assert wm.get("missing", "default") == "default"
        assert wm.get("missing") is None

    def test_delete(self):
        wm = WorkingMemory()
        wm.set("key1", "value1")
        wm.delete("key1")
        assert wm.get("key1") is None

    def test_clear(self):
        wm = WorkingMemory()
        wm.set("key1", "val1")
        wm.set("key2", "val2")
        wm.clear()
        assert wm.get_all() == {}

    def test_keys_order(self):
        wm = WorkingMemory()
        wm.set("b", 2)
        wm.set("a", 1)
        wm.set("c", 3)
        assert wm.keys() == ["b", "a", "c"]

    def test_format_for_context_empty(self):
        wm = WorkingMemory()
        assert wm.format_for_context() == ""

    def test_format_for_context(self):
        wm = WorkingMemory()
        wm.set("crime_count", 42)
        formatted = wm.format_for_context()
        assert "crime_count" in formatted
        assert "42" in formatted

    def test_overwrite(self):
        wm = WorkingMemory()
        wm.set("key1", "old")
        wm.set("key1", "new")
        assert wm.get("key1") == "new"
        assert wm.keys().count("key1") == 1
