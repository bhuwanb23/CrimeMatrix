from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CrimeCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    crime_type_id: Optional[int] = None
    district_id: Optional[int] = None
    location_id: Optional[int] = None
    priority: str = "medium"
    reported_by: Optional[int] = None


class CrimeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    crime_type_id: Optional[int] = None
    district_id: Optional[int] = None
    location_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None


class CrimeResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    crime_type_id: Optional[int]
    district_id: Optional[int]
    location_id: Optional[int]
    status: str
    priority: str
    reported_by: Optional[int]
    occurred_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
