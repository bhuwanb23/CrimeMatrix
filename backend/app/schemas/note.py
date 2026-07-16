from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class NoteCreate(BaseModel):
    investigation_id: int
    content: str = Field(..., min_length=1)
    author_id: Optional[int] = None


class NoteResponse(BaseModel):
    id: int
    investigation_id: int
    content: str
    author_id: Optional[int]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
