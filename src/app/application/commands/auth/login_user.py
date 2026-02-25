from typing import TYPE_CHECKING

from app.application.common.dto.base import dto
from app.application.common.dto.user import UserRead
from app.application.errors.auth import AuthenticationError
from app.application.interfaces.auth.jwt_provider import IJWTProvider, TokenPayload
from app.application.interfaces.auth.password_hasher import IPasswordHasher
from app.application.interfaces.interactor import Interactor
from app.application.interfaces.user.user_repository import IUserRepository


if TYPE_CHECKING:
    from app.domain.entities.user import User


@dto
class LoginUserRequest:
    username: str
    password: str


@dto
class LoginUserResponse:
    access_token: str
    refresh_token: str
    user: UserRead


class LoginUser(Interactor[LoginUserRequest, LoginUserResponse]):
    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
        jwt_provider: IJWTProvider,
    ) -> None:
        self._user_repository: IUserRepository = user_repository
        self._password_hasher: IPasswordHasher = password_hasher
        self._jwt_provider: IJWTProvider = jwt_provider

    async def execute(self, request: LoginUserRequest) -> LoginUserResponse:
        user: User | None = await self._user_repository.find_by_username(request.username)
        if user is None:
            raise AuthenticationError("Invalid username or password")

        is_valid: bool = self._password_hasher.verify_password(
            request.password,
            user.password_hash,
        )
        if not is_valid:
            raise AuthenticationError("Invalid username or password")

        payload = TokenPayload(sub=user.id, role=user.role)
        access_token: str = self._jwt_provider.create_access_token(payload)
        refresh_token: str = self._jwt_provider.create_refresh_token(payload)

        return LoginUserResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserRead(
                id=user.id,
                username=user.username,
                role=user.role,
            ),
        )
