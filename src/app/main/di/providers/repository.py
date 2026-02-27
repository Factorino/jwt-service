from dishka import BaseScope, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.user.user_repository import IUserRepository
from app.infrastructure.database.repositories.user_repository import SAUserRepository


class RepositoryProvider(Provider):
    scope: BaseScope | None = Scope.REQUEST

    @provide
    def user_repository(self, session: AsyncSession) -> IUserRepository:
        return SAUserRepository(session)
