from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TimelineEventCreate(BaseModel):
    investigation_id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    event_type: str = Field(..., min_length=1)
    event_date: Optional[datetime] = None


class TimelineEventResponse(BaseModel):
    id: int
    investigation_id: int
    title: str
    description: Optional[str]
    event_type: str
    event_date: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
