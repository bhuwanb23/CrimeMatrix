from pydantic import BaseModel, Field
from typing import Optional


class CrimeTypeCreate(BaseModel):
    name: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)
    description: Optional[str] = None
    severity_level: int = 1


class CrimeTypeResponse(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str]
    severity_level: int
    is_active: int

    class Config:
        from_attributes = True
