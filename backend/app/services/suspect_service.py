from app.services.base import BaseService
from app.repositories.suspect_repo import SuspectRepository
from app.models.suspect import Suspect
from typing import List


class SuspectService(BaseService[Suspect]):
    def __init__(self, repository: SuspectRepository):
        super().__init__(repository)

    async def get_by_status(self, status: str) -> List[Suspect]:
        return await self.repo.get_by_status(status)

    async def get_high_risk(self, min_score: float = 70.0) -> List[Suspect]:
        return await self.repo.get_high_risk(min_score)

    async def search_suspects(self, query: str) -> List[Suspect]:
        return await self.repo.search(query)
