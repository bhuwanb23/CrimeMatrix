import json
from typing import AsyncGenerator
from sse_starlette.sse import EventSourceResponse


class SSEChunk:
    def __init__(self, event: str = "message", data: str = "", done: bool = False):
        self.event = event
        self.data = data
        self.done = done

    def to_dict(self) -> dict:
        return {"event": self.event, "data": self.data, "done": self.done}


async def sse_response(generator: AsyncGenerator[str, None], done_event: str = "done"):
    async def event_generator():
        async for chunk in generator:
            yield {
                "event": "message",
                "data": json.dumps({"content": chunk, "done": False}),
            }
        yield {
            "event": done_event,
            "data": json.dumps({"content": "", "done": True}),
        }

    return EventSourceResponse(event_generator())
