from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CaseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    crime_type: str = Field(..., min_length=1)
    district: str = Field(..., min_length=1)
    priority: str = "medium"
    officer_id: Optional[int] = None
    fir_id: Optional[int] = None


class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    crime_type: Optional[str] = None
    district: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    officer_id: Optional[int] = None


class CaseResponse(BaseModel):
    id: int
    case_number: str
    title: str
    description: Optional[str]
    crime_type: str
    district: str
    status: str
    priority: str
    officer_id: Optional[int]
    fir_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
