from app.services.base import BaseService
from app.repositories.case_repo import CaseRepository
from app.models.case import Case
from typing import Optional, List


class CaseService(BaseService[Case]):
    def __init__(self, repository: CaseRepository):
        super().__init__(repository)

    async def get_by_number(self, case_number: str) -> Optional[Case]:
        return await self.repo.get_by_number(case_number)

    async def get_by_crime_no(self, crime_no: str) -> Optional[Case]:
        return await self.repo.get_by_crime_no(crime_no)

    async def get_by_district(self, district: str) -> List[Case]:
        return await self.repo.get_by_district(district)

    async def get_by_status(self, status: str) -> List[Case]:
        return await self.repo.get_by_status(status)

    async def get_by_category(self, case_category_id: int) -> List[Case]:
        return await self.repo.get_by_category(case_category_id)

    async def get_by_station(self, police_station_id: int) -> List[Case]:
        return await self.repo.get_by_station(police_station_id)

    async def search_cases(self, query: str) -> List[Case]:
        return await self.repo.search(query)
