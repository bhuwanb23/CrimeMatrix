from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FIRCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    crime_type: str = Field(..., min_length=1)
    district: str = Field(..., min_length=1)
    station: Optional[str] = None
    complainant_name: Optional[str] = None
    complainant_phone: Optional[str] = None


class FIRResponse(BaseModel):
    id: int
    fir_number: str
    title: str
    description: Optional[str]
    crime_type: str
    district: str
    station: Optional[str]
    status: str
    complainant_name: Optional[str]
    complainant_phone: Optional[str]
    date_filed: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
