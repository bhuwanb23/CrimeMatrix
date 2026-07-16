from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EvidenceCreate(BaseModel):
    case_id: int
    evidence_type: str = Field(..., min_length=1)
    description: Optional[str] = None
    file_path: Optional[str] = None
    recorded_by: Optional[int] = None


class EvidenceResponse(BaseModel):
    id: int
    case_id: int
    evidence_type: str
    description: Optional[str]
    status: str
    file_path: Optional[str]
    recorded_by: Optional[int]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
