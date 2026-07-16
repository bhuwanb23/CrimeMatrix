from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime


class APIResponse(BaseModel):
    success: bool = True
    data: Optional[Any] = None
    message: str = "Success"
    timestamp: str = ""

    def __init__(self, **kwargs):
        kwargs.setdefault("timestamp", datetime.utcnow().isoformat())
        super().__init__(**kwargs)


def success_response(data: Any = None, message: str = "Success"):
    return APIResponse(success=True, data=data, message=message)


def error_response(message: str, status_code: int = 400):
    return APIResponse(success=False, message=message)
