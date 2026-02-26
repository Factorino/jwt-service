from app.application.errors.base import ApplicationError


class AuthenticationError(ApplicationError):
    pass


class InvalidTokenError(AuthenticationError):
    pass


class TokenExpiredError(AuthenticationError):
    pass


class ForbiddenError(ApplicationError):
    pass
