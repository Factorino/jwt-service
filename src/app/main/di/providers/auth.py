from dishka import BaseScope, Provider, Scope, provide
from fastapi import Request

from app.application.interfaces.auth.identity_provider import IIdentityProvider
from app.application.interfaces.auth.jwt_provider import IJWTProvider
from app.application.interfaces.auth.password_hasher import IPasswordHasher
from app.application.interfaces.user.repository import IUserRepository
from app.infrastructure.auth.identity_provider import FastAPIIdentityProvider
from app.infrastructure.auth.jwt_provider import PyJWTProvider
from app.infrastructure.auth.password_hasher import BcryptPasswordHasher
from app.main.configs.jwt import JWTConfig


class AuthProvider(Provider):
    scope: BaseScope | None = Scope.APP

    @provide
    def password_hasher(self) -> IPasswordHasher:
        return BcryptPasswordHasher()

    @provide
    def jwt_provider(self, config: JWTConfig) -> IJWTProvider:
        return PyJWTProvider(
            public_key=config.public_key,
            private_key=config.private_key,
            algorithm=config.algorithm,
            access_ttl=config.access_ttl_minutes,
            refresh_ttl=config.refresh_ttl_minutes,
        )

    @provide(scope=Scope.REQUEST)
    def identity_provider(
        self,
        request: Request,
        jwt_provider: IJWTProvider,
        user_repository: IUserRepository,
    ) -> IIdentityProvider:
        token: str = request.headers.get("Authorization", "").removeprefix("Bearer ")
        return FastAPIIdentityProvider(
            token=token,
            jwt_provider=jwt_provider,
            user_repository=user_repository,
        )
