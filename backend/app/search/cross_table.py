from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.search.keyword import KeywordSearch
import structlog

logger = structlog.get_logger()


class CrossTableSearch:
    def __init__(self, db: AsyncSession):
        self.keyword_search = KeywordSearch(db)

    async def search(self, query: str, entities: List[str] = None) -> List[Dict]:
        target_entities = entities or ["cases", "crimes", "suspects", "persons", "vehicles"]
        results = await self.keyword_search.search(query, target_entities)

        # Deduplicate by id
        seen = set()
        unique = []
        for r in results:
            key = f"{r.get('entity')}_{r.get('id')}"
            if key not in seen:
                seen.add(key)
                unique.append(r)

        return unique
