from app.services.base import BaseService
from app.repositories.location_repo import LocationRepository
from app.models.location import Location


class LocationService(BaseService[Location]):
    def __init__(self, repository: LocationRepository):
        super().__init__(repository)
