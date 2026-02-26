from app.domain.errors.base import AppError


class ApplicationError(AppError):
    pass


class NotFoundError(ApplicationError):
    pass


class OperationFailedError(ApplicationError):
    pass


class DataMapperError(OperationFailedError):
    pass


class UnexpectedError(ApplicationError):
    pass
