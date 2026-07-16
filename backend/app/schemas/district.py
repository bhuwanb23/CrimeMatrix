from pydantic import BaseModel, Field
from typing import Optional


class DistrictCreate(BaseModel):
    name: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)
    state: str = "Karnataka"
    population: Optional[int] = None
    area_sq_km: Optional[int] = None


class DistrictResponse(BaseModel):
    id: int
    name: str
    code: str
    state: str
    population: Optional[int]
    area_sq_km: Optional[int]

    class Config:
        from_attributes = True
