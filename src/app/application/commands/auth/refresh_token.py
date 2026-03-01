from typing import TYPE_CHECKING

from app.application.common.dto.base import dto
from app.application.common.dto.user import UserRead
from app.application.errors.auth import AuthenticationError, InvalidTokenError
from app.application.interfaces.auth.jwt_provider import (
    IJWTProvider,
    TokenData,
    TokenPayload,
    TokenType,
)
from app.application.interfaces.common.interactor import Interactor
from app.application.interfaces.user.repository import IUserRepository


if TYPE_CHECKING:
    from app.domain.entities.user import User


@dto
class RefreshTokenRequest:
    refresh_token: str


@dto
class RefreshTokenResponse:
    access_token: str
    refresh_token: str
    user: UserRead


class RefreshToken(Interactor[RefreshTokenRequest, RefreshTokenResponse]):
    def __init__(
        self,
        user_repository: IUserRepository,
        jwt_provider: IJWTProvider,
    ) -> None:
        self._user_repository: IUserRepository = user_repository
        self._jwt_provider: IJWTProvider = jwt_provider

    async def execute(self, request: RefreshTokenRequest) -> RefreshTokenResponse:
        decoded: TokenData = self._jwt_provider.decode_token(request.refresh_token)

        if decoded.type != TokenType.REFRESH:
            raise InvalidTokenError(f"Token type must be '{TokenType.REFRESH}'")

        user: User | None = await self._user_repository.find_by_id(decoded.sub)
        if user is None:
            raise AuthenticationError("User no longer exists")

        payload = TokenPayload(sub=user.id, role=user.role)
        access_token: str = self._jwt_provider.create_access_token(payload)
        refresh_token: str = self._jwt_provider.create_refresh_token(payload)

        return RefreshTokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserRead(
                id=user.id,
                username=user.username,
                role=user.role,
            ),
        )
