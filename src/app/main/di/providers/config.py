from dishka import BaseScope, Provider, Scope, from_context
from dishka.dependency_source import CompositeDependencySource

from app.main.configs.api import APIConfig
from app.main.configs.config import Config
from app.main.configs.database import DatabaseConfig
from app.main.configs.jwt import JWTConfig


class ConfigProvider(Provider):
    scope: BaseScope | None = Scope.APP

    configs: CompositeDependencySource = (
        from_context(Config)
        + from_context(APIConfig)
        + from_context(DatabaseConfig)
        + from_context(JWTConfig)
    )
