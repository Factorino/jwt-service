from app.application.common.dto.base import dto
from app.application.common.dto.user import UserRead
from app.application.errors.base import NotFoundError
from app.application.interfaces.auth.identity_provider import IIdentityProvider
from app.application.interfaces.common.interactor import Interactor
from app.application.interfaces.user.repository import IUserRepository
from app.domain.entities.user import User
from app.domain.enums.user_role import UserRole


@dto
class GetUserByUsernameRequest:
    username: str


@dto
class GetUserByUsernameResponse:
    user: UserRead


class GetUserByUsername(Interactor[GetUserByUsernameRequest, GetUserByUsernameResponse]):
    def __init__(
        self,
        user_repository: IUserRepository,
        identity_provider: IIdentityProvider,
    ) -> None:
        self._user_repository: IUserRepository = user_repository
        self._idp: IIdentityProvider = identity_provider

    async def execute(self, request: GetUserByUsernameRequest) -> GetUserByUsernameResponse:
        user: User = await self._get_authorized_user(request)
        return GetUserByUsernameResponse(
            user=UserRead(
                id=user.id,
                username=user.username,
                role=user.role,
            ),
        )

    async def _get_authorized_user(self, request: GetUserByUsernameRequest) -> User:
        current_user: User = await self._idp.get_user()
        target_user: User | None = await self._user_repository.find_by_username(request.username)

        exception = NotFoundError(f"User with username '{request.username}' not found")

        if target_user is None:
            raise exception

        if current_user.role < UserRole.ADMIN and current_user.id != target_user.id:
            raise exception

        return target_user
