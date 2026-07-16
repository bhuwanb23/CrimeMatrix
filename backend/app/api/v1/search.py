from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from app.db.session import get_db
from app.search.base import SearchService
from app.search.keyword import KeywordSearch
from app.search.cross_table import CrossTableSearch
from app.core.response import success_response

router = APIRouter()


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    entities: Optional[List[str]] = None
    filters: Optional[List[Dict[str, Any]]] = None
    sort: Optional[Dict[str, str]] = None
    page: int = 1
    page_size: int = 20
    facets: Optional[List[str]] = None


class KeywordSearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    entities: Optional[List[str]] = None


@router.post("/")
async def universal_search(request: SearchRequest, db: AsyncSession = Depends(get_db)):
    svc = SearchService(db)
    result = await svc.search(
        query=request.query,
        entities=request.entities,
        filters=request.filters,
        sort=request.sort,
        page=request.page,
        page_size=request.page_size,
        facets=request.facets,
    )
    return success_response(data=result)


@router.post("/keyword")
async def keyword_search(request: KeywordSearchRequest, db: AsyncSession = Depends(get_db)):
    svc = KeywordSearch(db)
    results = await svc.search(request.query, request.entities)
    return success_response(data={"results": results, "total": len(results)})


@router.post("/advanced")
async def advanced_search(request: SearchRequest, db: AsyncSession = Depends(get_db)):
    svc = SearchService(db)
    result = await svc.search(
        query=request.query,
        entities=request.entities,
        filters=request.filters,
        sort=request.sort,
        page=request.page,
        page_size=request.page_size,
        facets=request.facets,
    )
    return success_response(data=result)


@router.get("/facets")
async def get_facets(entity: str = "cases", db: AsyncSession = Depends(get_db)):
    try:
        svc = SearchService(db)
        results = await svc.search(query="", entities=[entity])
        facet_fields = {
            "cases": ["crime_type", "district", "status"],
            "suspects": ["district", "status"],
            "persons": ["district", "gender"],
        }
        fields = facet_fields.get(entity, ["status"])
        facets = {}
        for field in fields:
            facets[field] = svc._compute_facets(results.get("results", []), field)
        return success_response(data={"entity": entity, "facets": facets})
    except Exception as e:
        return success_response(data={"entity": entity, "facets": {}, "error": str(e)})


@router.get("/suggestions")
async def search_suggestions(q: str = "", db: AsyncSession = Depends(get_db)):
    if len(q) < 2:
        return success_response(data={"suggestions": []})

    svc = SearchService(db)
    results = await svc.search(query=q, entities=["cases", "suspects"], page_size=5)
    suggestions = [r.get("title", r.get("name", "")) for r in results.get("results", [])]
    return success_response(data={"suggestions": suggestions[:5]})
