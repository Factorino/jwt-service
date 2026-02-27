from dishka import AsyncContainer, Provider, make_async_container

from app.main.configs.api import APIConfig
from app.main.configs.config import Config
from app.main.configs.database import DatabaseConfig
from app.main.configs.jwt import JWTConfig
from app.main.di.providers.auth import AuthProvider
from app.main.di.providers.config import ConfigProvider
from app.main.di.providers.database import DatabaseProvider
from app.main.di.providers.interactor import InteractorProvider
from app.main.di.providers.repository import RepositoryProvider


def create_container(config: Config) -> AsyncContainer:
    providers: list[Provider] = [
        ConfigProvider(),
        DatabaseProvider(),
        RepositoryProvider(),
        AuthProvider(),
        InteractorProvider(),
    ]
    context: dict[type, object] = {
        Config: config,
        APIConfig: config.api,
        DatabaseConfig: config.database,
        JWTConfig: config.jwt,
    }

    return make_async_container(*providers, context=context)
