from pydantic import BaseModel, Field
from typing import Optional


class CriminalCreate(BaseModel):
    person_id: Optional[int] = None
    alias: Optional[str] = None
    risk_score: float = 0.0
    status: str = "at_large"
    mo_description: Optional[str] = None
    behavioral_profile: Optional[str] = None


class CriminalUpdate(BaseModel):
    alias: Optional[str] = None
    risk_score: Optional[float] = None
    status: Optional[str] = None
    mo_description: Optional[str] = None
    behavioral_profile: Optional[str] = None


class CriminalResponse(BaseModel):
    id: int
    person_id: Optional[int]
    alias: Optional[str]
    risk_score: float
    status: str
    mo_description: Optional[str]
    behavioral_profile: Optional[str]

    class Config:
        from_attributes = True
