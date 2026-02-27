from dataclasses import field
from enum import StrEnum

from app.main.configs.api import APIConfig
from app.main.configs.base import config
from app.main.configs.database import DatabaseConfig
from app.main.configs.jwt import JWTConfig


class ConfigScope(StrEnum):
    API = "api"
    DATABASE = "database"
    JWT = "jwt"

    @staticmethod
    def from_config_type(config_type: type) -> str:
        if config_type is APIConfig:
            return ConfigScope.API
        if config_type is DatabaseConfig:
            return ConfigScope.DATABASE
        if config_type is JWTConfig:
            return ConfigScope.JWT
        raise ValueError(f"Unknown config type: {config_type}")


@config
class Config:
    api: APIConfig = field(default_factory=APIConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    jwt: JWTConfig = field(default_factory=JWTConfig)
