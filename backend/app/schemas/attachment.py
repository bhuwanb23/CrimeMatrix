from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AttachmentCreate(BaseModel):
    investigation_id: int
    filename: str = Field(..., min_length=1)
    file_path: str = Field(..., min_length=1)
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    uploaded_by: Optional[int] = None


class AttachmentResponse(BaseModel):
    id: int
    investigation_id: int
    filename: str
    file_path: str
    file_size: Optional[int]
    file_type: Optional[str]
    uploaded_by: Optional[int]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
