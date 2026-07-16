from app.services.base import BaseService
from app.repositories.case_repo import CaseRepository
from app.models.case import Case
from typing import Optional, List


class CaseService(BaseService[Case]):
    def __init__(self, repository: CaseRepository):
        super().__init__(repository)

    async def get_by_number(self, case_number: str) -> Optional[Case]:
        return await self.repo.get_by_number(case_number)

    async def get_by_district(self, district: str) -> List[Case]:
        return await self.repo.get_by_district(district)

    async def get_by_status(self, status: str) -> List[Case]:
        return await self.repo.get_by_status(status)

    async def search_cases(self, query: str) -> List[Case]:
        return await self.repo.search(query)
