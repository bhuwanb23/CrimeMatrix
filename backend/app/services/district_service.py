from app.services.base import BaseService
from app.repositories.district_repo import DistrictRepository
from app.models.district import District


class DistrictService(BaseService[District]):
    def __init__(self, repository: DistrictRepository):
        super().__init__(repository)
