from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BookmarkCreate(BaseModel):
    user_id: int
    investigation_id: int


class BookmarkResponse(BaseModel):
    id: int
    user_id: int
    investigation_id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
