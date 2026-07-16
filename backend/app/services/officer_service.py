from app.services.base import BaseService
from app.repositories.officer_repo import OfficerRepository
from app.models.officer import Officer
from typing import List


class OfficerService(BaseService[Officer]):
    def __init__(self, repository: OfficerRepository):
        super().__init__(repository)

    async def get_by_station(self, station_id: int) -> List[Officer]:
        return await self.repo.get_by_station(station_id)
