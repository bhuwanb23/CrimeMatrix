from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CaseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    crime_type: str = Field(..., min_length=1)
    district: str = Field(..., min_length=1)
    priority: str = "medium"
    officer_id: Optional[int] = None
    fir_id: Optional[int] = None
    # CaseMaster fields
    crime_no: Optional[str] = None
    incident_from_date: Optional[datetime] = None
    incident_to_date: Optional[datetime] = None
    info_received_ps_date: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    brief_facts: Optional[str] = None
    case_category_id: Optional[int] = None
    gravity_offence_id: Optional[int] = None
    crime_major_head_id: Optional[int] = None
    crime_minor_head_id: Optional[int] = None
    case_status_id: Optional[int] = None
    court_id: Optional[int] = None
    police_person_id: Optional[int] = None
    police_station_id: Optional[int] = None


class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    crime_type: Optional[str] = None
    district: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    officer_id: Optional[int] = None
    crime_no: Optional[str] = None
    incident_from_date: Optional[datetime] = None
    incident_to_date: Optional[datetime] = None
    info_received_ps_date: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    brief_facts: Optional[str] = None
    case_category_id: Optional[int] = None
    gravity_offence_id: Optional[int] = None
    crime_major_head_id: Optional[int] = None
    crime_minor_head_id: Optional[int] = None
    case_status_id: Optional[int] = None
    court_id: Optional[int] = None
    police_person_id: Optional[int] = None
    police_station_id: Optional[int] = None


class CaseResponse(BaseModel):
    id: int
    case_number: str
    crime_no: Optional[str] = None
    title: str
    description: Optional[str]
    crime_type: str
    district: str
    status: str
    priority: str
    officer_id: Optional[int]
    fir_id: Optional[int]
    # CaseMaster fields
    incident_from_date: Optional[datetime] = None
    incident_to_date: Optional[datetime] = None
    info_received_ps_date: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    brief_facts: Optional[str] = None
    case_category_id: Optional[int] = None
    gravity_offence_id: Optional[int] = None
    crime_major_head_id: Optional[int] = None
    crime_minor_head_id: Optional[int] = None
    case_status_id: Optional[int] = None
    court_id: Optional[int] = None
    police_person_id: Optional[int] = None
    police_station_id: Optional[int] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
