import json
from tools.base import Tool


class TranslatorTool(Tool):
    def __init__(self):
        self._translator = None

    def _get(self):
        if self._translator is None:
            from language.translator import Translator
            self._translator = Translator()
        return self._translator

    def get_name(self) -> str:
        return "translator"

    def get_description(self) -> str:
        return "Translate text between English and Kannada. Detects language automatically."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to translate"},
                "target_lang": {"type": "string", "description": "Target language: 'en' or 'kn'", "default": "en"},
            },
            "required": ["text"],
        }

    async def execute(self, text: str = "", target_lang: str = "en", **kwargs) -> str:
        result = self._get().translate(text, "auto", target_lang)
        return json.dumps(result)
