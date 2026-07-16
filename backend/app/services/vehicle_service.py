from app.services.base import BaseService
from app.repositories.vehicle_repo import VehicleRepository
from app.models.vehicle import Vehicle


class VehicleService(BaseService[Vehicle]):
    def __init__(self, repository: VehicleRepository):
        super().__init__(repository)

    async def get_by_registration(self, reg: str):
        return await self.repo.get_by_registration(reg)
