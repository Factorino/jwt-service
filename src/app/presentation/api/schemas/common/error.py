from typing import Any

from pydantic import BaseModel


class ErrorResponseSchema(BaseModel):
    status_code: int
    error_type: str
    message: str
    detail: dict[str, Any] = {}
