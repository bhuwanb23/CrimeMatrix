from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AlertCreate(BaseModel):
    alert_type: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: str = "medium"
    case_id: Optional[int] = None
    district: Optional[str] = None


class AlertResponse(BaseModel):
    id: int
    alert_type: str
    title: str
    description: Optional[str]
    priority: str
    status: str
    case_id: Optional[int]
    district: Optional[str]
    is_read: bool
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
