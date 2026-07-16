from pydantic import BaseModel, Field
from typing import Optional


class VictimCreate(BaseModel):
    person_id: Optional[int] = None
    case_id: Optional[int] = None
    statement: Optional[str] = None
    injury_type: Optional[str] = None


class VictimResponse(BaseModel):
    id: int
    person_id: Optional[int]
    case_id: Optional[int]
    statement: Optional[str]
    injury_type: Optional[str]
    status: str

    class Config:
        from_attributes = True
