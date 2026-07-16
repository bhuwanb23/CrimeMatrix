from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CaseStatusCreate(BaseModel):
    investigation_id: int
    new_status: str = Field(..., min_length=1)
    changed_by: Optional[int] = None
    notes: Optional[str] = None


class CaseStatusResponse(BaseModel):
    id: int
    investigation_id: int
    old_status: Optional[str]
    new_status: str
    changed_by: Optional[int]
    notes: Optional[str]
    changed_at: Optional[datetime]

    class Config:
        from_attributes = True
