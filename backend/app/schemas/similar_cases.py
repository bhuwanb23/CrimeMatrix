from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SimilarCaseResult(BaseModel):
    case_id: int
    case_number: str = ""
    title: str = ""
    crime_type: str = ""
    district: str = ""
    status: str = ""
    overall_score: float = 0
    mo_score: float = 0
    location_score: float = 0
    time_score: float = 0
    suspects_score: float = 0
    evidence_score: float = 0
    vehicles_score: float = 0
    reasons: List[str] = []


class SimilarCasesResponse(BaseModel):
    case_id: int
    similar_cases: List[SimilarCaseResult] = []
    count: int = 0
    computed_at: Optional[datetime] = None


class CompareResponse(BaseModel):
    case_1: dict = {}
    case_2: dict = {}
    dimension_scores: dict = {}
    overall_score: float = 0
    reasons: List[str] = []


class ComputeRequest(BaseModel):
    case_id: Optional[int] = None
    force: bool = False
