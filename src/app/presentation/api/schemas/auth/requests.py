from pydantic.dataclasses import dataclass

from app.application.commands.auth.refresh_token import RefreshTokenRequest
from app.application.commands.auth.register_user import RegisterUserRequest


@dataclass(frozen=True)
class RegisterUserRequestSchema(RegisterUserRequest):
    pass



@dataclass(frozen=True)
class RefreshTokenRequestSchema(RefreshTokenRequest):
    pass
