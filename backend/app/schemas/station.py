from pydantic import BaseModel, Field
from typing import Optional


class StationCreate(BaseModel):
    name: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)
    district_id: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    type: str = "police_station"


class StationResponse(BaseModel):
    id: int
    name: str
    code: str
    district_id: Optional[int]
    address: Optional[str]
    phone: Optional[str]
    type: str

    class Config:
        from_attributes = True
