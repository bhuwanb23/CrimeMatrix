from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class InvestigationCreate(BaseModel):
    case_id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: str = "medium"
    officer_id: Optional[int] = None


class InvestigationUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    progress: Optional[int] = None


class InvestigationResponse(BaseModel):
    id: int
    case_id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    officer_id: Optional[int]
    progress: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
