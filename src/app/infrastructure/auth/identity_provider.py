from app.application.errors.auth import InvalidTokenError
from app.application.errors.base import NotFoundError
from app.application.interfaces.auth.identity_provider import IIdentityProvider
from app.application.interfaces.auth.jwt_provider import IJWTProvider, TokenData, TokenType
from app.application.interfaces.user.user_repository import IUserRepository
from app.domain.entities.user import User


class FastAPIIdentityProvider(IIdentityProvider):
    def __init__(
        self,
        token: str,
        jwt_provider: IJWTProvider,
        user_repository: IUserRepository,
    ) -> None:
        self._token: str = token
        self._jwt_provider: IJWTProvider = jwt_provider
        self._user_repository: IUserRepository = user_repository
        self._cached_user: User | None = None

    async def get_user(self) -> User:
        if self._cached_user is not None:
            return self._cached_user

        user: User = await self._get_user_from_token()
        self._cached_user = user
        return user

    async def _get_user_from_token(self) -> User:
        decoded: TokenData = self._jwt_provider.decode_token(self._token)

        if decoded.type != TokenType.ACCESS:
            raise InvalidTokenError(f"Token type must be '{TokenType.ACCESS}'")

        user: User | None = await self._user_repository.find_by_id(decoded.sub)

        if user is None:
            raise NotFoundError("User not found")

        return user
