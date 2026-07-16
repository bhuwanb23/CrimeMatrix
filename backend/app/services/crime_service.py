from app.services.base import BaseService
from app.repositories.crime_repo import CrimeRepository
from app.models.crime import Crime
from typing import List


class CrimeService(BaseService[Crime]):
    def __init__(self, repository: CrimeRepository):
        super().__init__(repository)

    async def get_by_district(self, district_id: int) -> List[Crime]:
        return await self.repo.get_by_district(district_id)

    async def get_by_status(self, status: str) -> List[Crime]:
        return await self.repo.get_by_status(status)

    async def search_crimes(self, query: str) -> List[Crime]:
        return await self.repo.search(query)
