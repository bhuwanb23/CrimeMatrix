from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
import structlog
import time

logger = structlog.get_logger()


class SearchService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search(
        self,
        query: str,
        entities: List[str] = None,
        filters: List[Dict] = None,
        sort: Dict = None,
        page: int = 1,
        page_size: int = 20,
        facets: List[str] = None,
    ) -> Dict[str, Any]:
        start_time = time.time()

        results = []
        for entity in (entities or ["cases", "crimes", "suspects", "persons"]):
            entity_results = await self._search_entity(entity, query, filters, sort)
            results.extend(entity_results)

        # Apply pagination
        total = len(results)
        start = (page - 1) * page_size
        end = start + page_size
        paginated = results[start:end]

        # Compute facets
        facet_results = {}
        if facets:
            for facet_field in facets:
                facet_results[facet_field] = self._compute_facets(results, facet_field)

        query_time = round((time.time() - start_time) * 1000, 2)

        return {
            "results": paginated,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size if total > 0 else 0,
            "facets": facet_results,
            "query_time_ms": query_time,
        }

    async def _search_entity(self, entity: str, query: str, filters: List[Dict], sort: Dict) -> List[Dict]:
        try:
            if entity == "cases":
                from app.models.case import Case
                return await self._search_model(Case, query, filters, sort, {"entity": "case"})
            elif entity == "crimes":
                from app.models.crime import Crime
                return await self._search_model(Crime, query, filters, sort, {"entity": "crime"})
            elif entity == "suspects":
                from app.models.suspect import Suspect
                return await self._search_model(Suspect, query, filters, sort, {"entity": "suspect"})
            elif entity == "persons":
                from app.models.person import Person
                return await self._search_model(Person, query, filters, sort, {"entity": "person"})
            elif entity == "criminals":
                from app.models.criminal import Criminal
                return await self._search_model(Criminal, query, filters, sort, {"entity": "criminal"})
            elif entity == "vehicles":
                from app.models.vehicle import Vehicle
                return await self._search_model(Vehicle, query, filters, sort, {"entity": "vehicle"})
            elif entity == "phones":
                from app.models.phone import Phone
                return await self._search_model(Phone, query, filters, sort, {"entity": "phone"})
            return []
        except Exception as e:
            logger.error("search_entity_error", entity=entity, error=str(e))
            return []

    async def _search_model(self, model, query: str, filters: List[Dict], sort: Dict, metadata: Dict) -> List[Dict]:
        from sqlalchemy import inspect as sqla_inspect

        mapper = sqla_inspect(model)
        string_columns = [c.key for c in mapper.columns if c.type.__class__.__name__ in ('String', 'Text')]

        conditions = []
        if query:
            for col in string_columns:
                conditions.append(getattr(model, col).ilike(f"%{query}%"))

        stmt = select(model)
        if conditions:
            stmt = stmt.where(or_(*conditions))

        result = await self.db.execute(stmt)
        items = result.scalars().all()

        results = []
        for item in items:
            item_dict = {c.key: getattr(item, c.key) for c in mapper.columns}
            item_dict["entity"] = metadata.get("entity", "unknown")
            item_dict["id"] = item.id
            results.append(item_dict)

        return results

    def _compute_facets(self, results: List[Dict], field: str) -> Dict[str, int]:
        facets = {}
        for item in results:
            value = item.get(field, "unknown")
            if isinstance(value, str):
                facets[value] = facets.get(value, 0) + 1
        return dict(sorted(facets.items(), key=lambda x: x[1], reverse=True))
