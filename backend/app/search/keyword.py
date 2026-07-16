from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
import structlog

logger = structlog.get_logger()


class KeywordSearch:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search(self, query: str, entities: List[str] = None) -> List[Dict]:
        results = []
        for entity in (entities or ["cases", "crimes", "suspects"]):
            entity_results = await self._search_entity(entity, query)
            results.extend(entity_results)
        return results

    async def _search_entity(self, entity: str, query: str) -> List[Dict]:
        try:
            if entity == "cases":
                from app.models.case import Case
                return await self._search(Case, query)
            elif entity == "crimes":
                from app.models.crime import Crime
                return await self._search(Crime, query)
            elif entity == "suspects":
                from app.models.suspect import Suspect
                return await self._search(Suspect, query)
            elif entity == "persons":
                from app.models.person import Person
                return await self._search(Person, query)
            return []
        except Exception as e:
            logger.error("keyword_search_error", entity=entity, error=str(e))
            return []

    async def _search(self, model, query: str) -> List[Dict]:
        from sqlalchemy import inspect as sqla_inspect
        mapper = sqla_inspect(model)
        string_cols = [c.key for c in mapper.columns if c.type.__class__.__name__ in ('String', 'Text')]

        conditions = [getattr(model, col).ilike(f"%{query}%") for col in string_cols]
        result = await self.db.execute(select(model).where(or_(*conditions)))

        return [
            {c.key: getattr(item, c.key) for c in mapper.columns}
            for item in result.scalars().all()
        ]
