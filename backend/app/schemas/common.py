from pydantic import BaseModel, Field
from typing import Any, Optional, List, Generic, TypeVar
from datetime import datetime

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int


class FilterParams(BaseModel):
    field: str
    operator: str = "eq"  # eq, ne, gt, lt, gte, lte, in, like
    value: Any


class SortParams(BaseModel):
    field: str
    direction: str = "desc"  # asc, desc


class SearchParams(BaseModel):
    query: str = Field(..., min_length=1)
    fields: List[str] = ["title", "description"]


class APIResponse(BaseModel):
    success: bool = True
    data: Optional[Any] = None
    message: str = "Success"
    timestamp: str = ""

    def __init__(self, **kwargs):
        kwargs.setdefault("timestamp", datetime.utcnow().isoformat())
        super().__init__(**kwargs)
