import pytest
from memory.preferences import UserPreferences


class TestUserPreferences:
    def test_get_defaults(self):
        prefs = UserPreferences()
        d = prefs.get("user1")
        assert d["language"] == "en"
        assert d["response_style"] == "concise"
        assert d["timezone"] == "Asia/Kolkata"

    def test_set_and_get(self):
        prefs = UserPreferences()
        prefs.set("user1", "language", "hi")
        assert prefs.get("user1")["language"] == "hi"

    def test_user_isolation(self):
        prefs = UserPreferences()
        prefs.set("user1", "language", "hi")
        prefs.set("user2", "language", "kn")
        assert prefs.get("user1")["language"] == "hi"
        assert prefs.get("user2")["language"] == "kn"

    def test_update(self):
        prefs = UserPreferences()
        prefs.update("user1", {"language": "kn", "response_style": "detailed"})
        d = prefs.get("user1")
        assert d["language"] == "kn"
        assert d["response_style"] == "detailed"

    def test_delete(self):
        prefs = UserPreferences()
        prefs.set("user1", "language", "hi")
        prefs.delete("user1")
        d = prefs.get("user1")
        assert d["language"] == "en"

    def test_format_for_system_prompt_new_user_returns_defaults(self):
        prefs = UserPreferences()
        result = prefs.format_for_system_prompt("new_user")
        assert "language" in result
        assert "en" in result

    def test_format_for_system_prompt(self):
        prefs = UserPreferences()
        prefs.set("user1", "language", "hi")
        result = prefs.format_for_system_prompt("user1")
        assert "hi" in result
