from dishka import BaseScope, Provider, Scope, provide

from app.application.commands.auth.login_user import LoginUser
from app.application.commands.auth.refresh_token import RefreshToken
from app.application.commands.auth.register_user import RegisterUser
from app.application.interfaces.auth.identity_provider import IIdentityProvider
from app.application.interfaces.auth.jwt_provider import IJWTProvider
from app.application.interfaces.auth.password_hasher import IPasswordHasher
from app.application.interfaces.common.transaction_manager import ITransactionManager
from app.application.interfaces.user.repository import IUserRepository
from app.application.queries.user.get_by_username import GetUserByUsername
from app.application.queries.user.get_me import GetMe


class InteractorProvider(Provider):
    scope: BaseScope | None = Scope.REQUEST

    @provide
    def register_user(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
        transaction_manager: ITransactionManager,
    ) -> RegisterUser:
        return RegisterUser(user_repository, password_hasher, transaction_manager)

    @provide
    def login_user(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
        jwt_provider: IJWTProvider,
    ) -> LoginUser:
        return LoginUser(user_repository, password_hasher, jwt_provider)

    @provide
    def refresh_token(
        self,
        user_repository: IUserRepository,
        jwt_provider: IJWTProvider,
    ) -> RefreshToken:
        return RefreshToken(user_repository, jwt_provider)

    @provide
    def get_me(
        self,
        identity_provider: IIdentityProvider,
    ) -> GetMe:
        return GetMe(identity_provider)

    @provide
    def get_user_by_username(
        self,
        user_repository: IUserRepository,
        identity_provider: IIdentityProvider,
    ) -> GetUserByUsername:
        return GetUserByUsername(user_repository, identity_provider)
