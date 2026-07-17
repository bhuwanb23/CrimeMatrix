import json
import httpx
from tools.base import Tool


class WebFetchTool(Tool):
    def get_name(self) -> str:
        return "web_fetch"

    def get_description(self) -> str:
        return "Fetch content from a URL. Returns the page content as text."

    def get_parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to fetch",
                }
            },
            "required": ["url"],
        }

    async def execute(self, url: str = "", **kwargs) -> str:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0, follow_redirects=True)
                text = response.text[:5000]
                return json.dumps({"status": response.status_code, "content": text})
        except Exception as e:
            return json.dumps({"error": str(e)})
