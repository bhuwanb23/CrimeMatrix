from pydantic import BaseModel, Field
from typing import Optional


class VehicleCreate(BaseModel):
    registration_number: str = Field(..., min_length=1)
    make: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    type: Optional[str] = None
    owner_id: Optional[int] = None


class VehicleResponse(BaseModel):
    id: int
    registration_number: str
    make: Optional[str]
    model: Optional[str]
    color: Optional[str]
    type: Optional[str]
    owner_id: Optional[int]
    status: str

    class Config:
        from_attributes = True
