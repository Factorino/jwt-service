from collections.abc import Callable
from types import MappingProxyType
from typing import Any

from pydantic import BaseModel

from app.application.errors.base import DataMapperError


def get_mapper(
    mapping: MappingProxyType[type[BaseModel], Callable[[BaseModel], Any]],
) -> Callable[[BaseModel], Any]:
    def _mapper(schema: BaseModel) -> Any:
        schema_type = type(schema)
        converter: Callable[[BaseModel], Any] | None = mapping.get(schema_type)
        if converter is None:
            raise DataMapperError(f"No mapper provided for schema {schema_type.__name__}")
        return converter(schema)

    return _mapper
