from app.services.base import BaseService
from app.repositories.crimetype_repo import CrimeTypeRepository
from app.models.crimetype import CrimeType


class CrimeTypeService(BaseService[CrimeType]):
    def __init__(self, repository: CrimeTypeRepository):
        super().__init__(repository)
