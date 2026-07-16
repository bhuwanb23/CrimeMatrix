from app.services.base import BaseService
from app.repositories.station_repo import StationRepository
from app.models.station import Station


class StationService(BaseService[Station]):
    def __init__(self, repository: StationRepository):
        super().__init__(repository)
