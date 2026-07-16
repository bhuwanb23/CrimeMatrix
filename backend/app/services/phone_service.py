from app.services.base import BaseService
from app.repositories.phone_repo import PhoneRepository
from app.models.phone import Phone


class PhoneService(BaseService[Phone]):
    def __init__(self, repository: PhoneRepository):
        super().__init__(repository)

    async def get_by_number(self, number: str):
        return await self.repo.get_by_number(number)
