from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.domain.entities.user import User


class IUserRepository(Protocol):
    @abstractmethod
    async def find_by_id(self, id: UUID) -> User | None: ...

    @abstractmethod
    async def find_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    async def add(self, user: User) -> User: ...

    @abstractmethod
    async def delete(self, user: User) -> bool: ...
