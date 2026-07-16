from app.services.base import BaseService
from app.repositories.user_repo import UserRepository
from app.models.user import User
from typing import Optional


class UserService(BaseService[User]):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)

    async def get_by_username(self, username: str) -> Optional[User]:
        return await self.repo.get_by_username(username)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.repo.get_by_email(email)

    async def create_user(self, data: dict) -> User:
        return await self.repo.create(data)
