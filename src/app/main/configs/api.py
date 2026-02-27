from dataclasses import field
from enum import StrEnum

from app.main.configs.base import config


class Envirenment(StrEnum):
    DEV = "development"
    PROD = "production"
    TEST = "testing"


@config
class CorsConfig:
    allow_origins: list[str] = field(default=["*"])
    allow_credentials: bool = False
    allow_methods: list[str] = field(default=["*"])
    allow_headers: list[str] = field(default=["*"])
    max_age: int = 600


@config
class APIConfig:
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    debug: bool = False
    environment: Envirenment = Envirenment.DEV

    cors: CorsConfig = field(default_factory=CorsConfig)
