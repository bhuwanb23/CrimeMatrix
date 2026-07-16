from app.services.base import BaseService
from app.repositories.victim_repo import VictimRepository
from app.models.victim import Victim


class VictimService(BaseService[Victim]):
    def __init__(self, repository: VictimRepository):
        super().__init__(repository)
