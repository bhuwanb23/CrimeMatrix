from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class InvestigationCreate(BaseModel):
    case_id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: str = "active"
    priority: str = "medium"
    officer_id: Optional[int] = None
    progress: int = 0
    district: Optional[str] = None


class InvestigationUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    officer_id: Optional[int] = None
    progress: Optional[int] = None
    district: Optional[str] = None


class InvestigationResponse(BaseModel):
    id: int
    case_id: Optional[int]
    title: str
    description: Optional[str]
    status: str
    priority: str
    progress: int
    district: Optional[str]
    officer_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    # Nested data
    notes: List[dict] = []
    evidence: List[dict] = []
    timeline: List[dict] = []
    case_links: List[dict] = []
    status_logs: List[dict] = []
    attachments: List[dict] = []

    class Config:
        from_attributes = True


class InvestigationListItem(BaseModel):
    id: int
    case_id: Optional[int]
    title: str
    status: str
    priority: str
    progress: int
    district: Optional[str]
    officer_id: Optional[int]
    created_at: Optional[datetime]
    notes_count: int = 0
    evidence_count: int = 0
    timeline_count: int = 0

    class Config:
        from_attributes = True
