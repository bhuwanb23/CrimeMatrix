from pydantic import BaseModel, Field
from typing import Optional


class OfficerCreate(BaseModel):
    badge_number: str = Field(..., min_length=1)
    rank: Optional[str] = None
    station_id: Optional[int] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None


class OfficerResponse(BaseModel):
    id: int
    badge_number: str
    rank: Optional[str]
    station_id: Optional[int]
    specialization: Optional[str]
    phone: Optional[str]
    status: str

    class Config:
        from_attributes = True
