from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CaseLinkCreate(BaseModel):
    investigation_id: int
    linked_case_id: int
    link_type: str = Field(..., min_length=1)
    description: Optional[str] = None


class CaseLinkResponse(BaseModel):
    id: int
    investigation_id: int
    linked_case_id: int
    link_type: str
    description: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
