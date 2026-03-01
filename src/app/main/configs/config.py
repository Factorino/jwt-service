from dataclasses import field
from enum import StrEnum
from types import MappingProxyType
from typing import Final

from app.main.configs.api import APIConfig, CorsConfig
from app.main.configs.base import config
from app.main.configs.database import DatabaseConfig
from app.main.configs.jwt import JWTConfig


class ConfigScope(StrEnum):
    API = "api"
    CORS = "cors"
    DATABASE = "database"
    JWT = "jwt"

    @staticmethod
    def from_config_type(config_type: type) -> str | None:
        return _MAPPING.get(config_type)


_MAPPING: Final[MappingProxyType[type, str]] = MappingProxyType(
    {
        APIConfig: ConfigScope.API,
        CorsConfig: ConfigScope.CORS,
        DatabaseConfig: ConfigScope.DATABASE,
        JWTConfig: ConfigScope.JWT,
    }
)


@config
class Config:
    api: APIConfig = field(default_factory=APIConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    jwt: JWTConfig = field(default_factory=JWTConfig)
