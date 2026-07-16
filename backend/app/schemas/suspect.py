from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SuspectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: Optional[int] = None
    gender: Optional[str] = None
    district: Optional[str] = None
    description: Optional[str] = None
    physical_description: Optional[str] = None
    aliases: Optional[str] = None


class SuspectUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    district: Optional[str] = None
    status: Optional[str] = None
    risk_score: Optional[float] = None
    description: Optional[str] = None
    physical_description: Optional[str] = None
    aliases: Optional[str] = None


class SuspectResponse(BaseModel):
    id: int
    name: str
    age: Optional[int]
    gender: Optional[str]
    district: Optional[str]
    status: str
    risk_score: float
    description: Optional[str]
    physical_description: Optional[str]
    aliases: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
