from app.services.base import BaseService
from app.repositories.witness_repo import WitnessRepository
from app.models.witness import Witness


class WitnessService(BaseService[Witness]):
    def __init__(self, repository: WitnessRepository):
        super().__init__(repository)
