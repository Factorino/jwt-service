from pydantic import BaseModel

from app.presentation.api.schemas.user.responses import UserSchema


class RegisterUserResponseSchema(BaseModel):
    user: UserSchema


class LoginUserResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"  # noqa: S105
    user: UserSchema


class RefreshTokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"  # noqa: S105
    user: UserSchema
