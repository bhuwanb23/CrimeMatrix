from pydantic import BaseModel, Field
from typing import Optional


class PersonCreate(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    district: Optional[str] = None
    aadhar_number: Optional[str] = None


class PersonUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class PersonResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: Optional[str]
    gender: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    district: Optional[str]

    class Config:
        from_attributes = True
