from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ComplainantCreate(BaseModel):
    case_id: int
    name: str = Field(..., min_length=1, max_length=200)
    age_year: Optional[int] = None
    occupation_id: Optional[int] = None
    religion_id: Optional[int] = None
    caste_id: Optional[int] = None
    gender_id: Optional[int] = None


class ComplainantUpdate(BaseModel):
    name: Optional[str] = None
    age_year: Optional[int] = None
    occupation_id: Optional[int] = None
    religion_id: Optional[int] = None
    caste_id: Optional[int] = None
    gender_id: Optional[int] = None


class ComplainantResponse(BaseModel):
    id: int
    case_id: int
    name: str
    age_year: Optional[int] = None
    occupation_id: Optional[int] = None
    occupation_name: Optional[str] = None
    religion_id: Optional[int] = None
    religion_name: Optional[str] = None
    caste_id: Optional[int] = None
    caste_name: Optional[str] = None
    gender_id: Optional[int] = None
    gender_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
