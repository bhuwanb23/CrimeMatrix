from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000)
    provider: Optional[str] = Field(default=None)
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    response: str
    provider: str
    model: str
    tokens_used: Optional[int] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    uptime: float
    environment: str
