from pydantic import BaseModel, Field
from typing import Optional


class WitnessCreate(BaseModel):
    person_id: Optional[int] = None
    case_id: Optional[int] = None
    statement: Optional[str] = None
    reliability: str = "unknown"


class WitnessResponse(BaseModel):
    id: int
    person_id: Optional[int]
    case_id: Optional[int]
    statement: Optional[str]
    reliability: str

    class Config:
        from_attributes = True
