from collections.abc import Callable
from uuid import UUID

from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.user.user_repository import IUserRepository
from app.domain.entities.user import User
from app.infrastructure.database.mapper import get_mapper
from app.infrastructure.database.models.user import UserORM
from app.infrastructure.database.repositories.base_repository import SABaseRepository


_to_domain: Callable[[UserORM], User] = get_mapper(UserORM, User)
_to_orm: Callable[[User], UserORM] = get_mapper(User, UserORM)


class SAUserRepository(IUserRepository, SABaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session
        super().__init__(session)

    async def find_by_id(self, id: UUID) -> User | None:
        query: Select[tuple[UserORM]] = select(UserORM).where(UserORM.id == id)
        result: Result[tuple[UserORM]] = await self._execute(query)
        orm_user: UserORM | None = result.scalar_one_or_none()

        if orm_user is None:
            return None

        return _to_domain(orm_user)

    async def find_by_username(self, username: str) -> User | None:
        query: Select[tuple[UserORM]] = select(UserORM).where(UserORM.username == username)
        result: Result[tuple[UserORM]] = await self._execute(query)
        orm_user: UserORM | None = result.scalar_one_or_none()

        if orm_user is None:
            return None

        return _to_domain(orm_user)

    async def add(self, user: User) -> User:
        orm_user: UserORM = _to_orm(user)
        self._session.add(orm_user)
        return user

    async def delete(self, user: User) -> bool:
        stmt: Select[tuple[UserORM]] = select(UserORM).where(UserORM.id == user.id)
        result: Result[tuple[UserORM]] = await self._execute(stmt)
        orm_user: UserORM | None = result.scalar_one_or_none()

        if orm_user is None:
            return False

        await self._session.delete(orm_user)
        return True
