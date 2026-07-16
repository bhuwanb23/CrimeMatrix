from app.services.base import BaseService
from app.repositories.criminal_repo import CriminalRepository
from app.models.criminal import Criminal
from typing import List


class CriminalService(BaseService[Criminal]):
    def __init__(self, repository: CriminalRepository):
        super().__init__(repository)

    async def get_by_status(self, status: str) -> List[Criminal]:
        return await self.repo.get_by_status(status)

    async def get_high_risk(self, min_score: float = 70.0) -> List[Criminal]:
        return await self.repo.get_high_risk(min_score)
