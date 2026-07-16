from pydantic import BaseModel, Field
from typing import Optional


class LocationCreate(BaseModel):
    name: str = Field(..., min_length=1)
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    district_id: Optional[int] = None
    type: Optional[str] = None


class LocationResponse(BaseModel):
    id: int
    name: str
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    district_id: Optional[int]
    type: Optional[str]

    class Config:
        from_attributes = True
