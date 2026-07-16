from pydantic import BaseModel, Field
from typing import Optional


class PhoneCreate(BaseModel):
    number: str = Field(..., min_length=1)
    owner_id: Optional[int] = None
    carrier: Optional[str] = None
    type: str = "mobile"


class PhoneResponse(BaseModel):
    id: int
    number: str
    owner_id: Optional[int]
    carrier: Optional[str]
    type: str
    status: str

    class Config:
        from_attributes = True
