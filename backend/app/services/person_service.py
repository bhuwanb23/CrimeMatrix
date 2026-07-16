from app.services.base import BaseService
from app.repositories.person_repo import PersonRepository
from app.models.person import Person
from typing import List


class PersonService(BaseService[Person]):
    def __init__(self, repository: PersonRepository):
        super().__init__(repository)

    async def search_persons(self, query: str) -> List[Person]:
        return await self.repo.search(query)
