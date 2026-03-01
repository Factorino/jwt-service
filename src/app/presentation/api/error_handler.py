from types import MappingProxyType
from typing import Any, Final

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.application.errors.auth import (
    AccessDeniedError,
    AuthenticationError,
)
from app.application.errors.base import (
    NotFoundError,
    OperationFailedError,
    UnexpectedError,
)
from app.domain.errors.base import (
    AlreadyExistsError,
    AppError,
    ValidationError,
)
from app.presentation.api.schemas.common.error import ErrorResponseSchema


ERROR_STATUS_CODE: Final[MappingProxyType[type[AppError], int]] = MappingProxyType(
    {
        # Domain errors
        ValidationError: status.HTTP_400_BAD_REQUEST,
        AlreadyExistsError: status.HTTP_409_CONFLICT,
        # Application errors
        AuthenticationError: status.HTTP_401_UNAUTHORIZED,
        AccessDeniedError: status.HTTP_403_FORBIDDEN,
        NotFoundError: status.HTTP_404_NOT_FOUND,
        OperationFailedError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        # Fallback errors
        UnexpectedError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        AppError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }
)


def get_error_status_code(exception: Exception) -> int:
    for cls in type(exception).mro():
        if cls in ERROR_STATUS_CODE:
            return ERROR_STATUS_CODE[cls]
    return status.HTTP_500_INTERNAL_SERVER_ERROR


def get_error_type(exception: Exception) -> str:
    return type(exception).__qualname__


def get_error_message(exception: Exception) -> str:
    return str(exception) if exception.args else "Unexpected error"


async def app_error_handler(_request: Request, exception: Exception) -> JSONResponse:
    error: AppError = exception if isinstance(exception, AppError) else UnexpectedError()
    error_status_code: int = get_error_status_code(error)
    error_type: str = get_error_type(error)
    error_message: str = get_error_message(error)

    error_response: dict[str, Any] = ErrorResponseSchema(
        status_code=error_status_code,
        error_type=error_type,
        message=error_message,
    ).model_dump(mode="json")

    return JSONResponse(
        status_code=error_status_code,
        content=error_response,
    )
