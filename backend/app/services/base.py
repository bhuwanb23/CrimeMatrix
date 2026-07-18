from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.schemas.common import PaginatedResponse, PaginationParams, FilterParams, SortParams, SearchParams

ModelType = TypeVar("ModelType")


class BaseService(Generic[ModelType]):
    def __init__(self, repository: BaseRepository[ModelType]):
        self.repo = repository

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        return await self.repo.get_by_id(id)

    async def get_paginated(self, params: PaginationParams) -> PaginatedResponse:
        from sqlalchemy import func as sql_func
        items = await self.repo.get_all(skip=params.offset, limit=params.page_size)
        total_result = await self.repo.db.execute(sql_func.count(self.repo.model.id))
        total = total_result.scalar()
        return PaginatedResponse(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=(total + params.page_size - 1) // params.page_size,
        )

    async def create(self, data: Dict[str, Any]) -> ModelType:
        return await self.repo.create(data)

    async def update(self, id: int, data: Dict[str, Any]) -> Optional[ModelType]:
        return await self.repo.update(id, data)

    async def delete(self, id: int) -> bool:
        return await self.repo.delete(id)

    async def search(self, query: str) -> List[ModelType]:
        if hasattr(self.repo, 'search'):
            return await self.repo.search(query)
        return []

    def apply_filters(self, items: List[ModelType], filters: List[FilterParams]) -> List[ModelType]:
        result = items
        for f in filters:
            if f.operator == "eq":
                result = [i for i in result if getattr(i, f.field, None) == f.value]
            elif f.operator == "like":
                result = [i for i in result if f.value.lower() in str(getattr(i, f.field, "")).lower()]
            elif f.operator == "gt":
                result = [i for i in result if getattr(i, f.field, 0) > f.value]
            elif f.operator == "lt":
                result = [i for i in result if getattr(i, f.field, 0) < f.value]
        return result

    def apply_sort(self, items: List[ModelType], sort: SortParams) -> List[ModelType]:
        reverse = sort.direction == "desc"
        return sorted(items, key=lambda x: getattr(x, sort.field, ""), reverse=reverse)
