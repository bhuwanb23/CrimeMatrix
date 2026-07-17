import json
from tools.base import Tool


class IdentityMatchTool(Tool):
    def __init__(self):
        self._matcher = None

    def _get_matcher(self):
        if self._matcher is None:
            from identity.name_matcher import IndianNameMatcher
            self._matcher = IndianNameMatcher()
        return self._matcher

    def get_name(self) -> str:
        return "identity_match"

    def get_description(self) -> str:
        return "Match two Indian names and return similarity score (0-100). Supports nicknames, transliteration variants, and phonetic matching."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "name1": {"type": "string", "description": "First name to compare"},
                "name2": {"type": "string", "description": "Second name to compare"},
            },
            "required": ["name1", "name2"],
        }

    async def execute(self, name1: str = "", name2: str = "", **kwargs) -> str:
        matcher = self._get_matcher()
        result = matcher.match(name1, name2)
        return json.dumps(result)
