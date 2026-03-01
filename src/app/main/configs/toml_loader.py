import os
import tomllib
from typing import Any

from adaptix import Retort

from app.application.errors.base import DataMapperError
from app.main.configs.config import ConfigScope


DEFAULT_CONFIG_PATH = "./config/config.toml"


_retort = Retort()


def read_toml(path: str) -> dict[str, Any]:
    try:
        with open(path, mode="rb") as file:
            return tomllib.load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Config file not found: {path}") from e
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"Invalid TOML in {path}") from e


def load_config[CfgT](
    type: type[CfgT],
    path: str | None = None,
) -> CfgT:
    if path is None:
        path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)

    data: dict[str, Any] = read_toml(path)

    scope: str | None = ConfigScope.from_config_type(type)
    if scope:
        data = data.get(scope, {})

    try:
        return _retort.load(data, type)
    except Exception as e:
        raise DataMapperError(f"Failed to load config: {type.__name__}") from e
