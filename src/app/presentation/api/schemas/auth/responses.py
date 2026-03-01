from app.presentation.api.schemas.common.response import BaseResponseSchema
from app.presentation.api.schemas.user.responses import UserSchema


class RegisterUserResponseSchema(BaseResponseSchema):
    user: UserSchema


class LoginUserResponseSchema(BaseResponseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"  # noqa: S105
    user: UserSchema


class RefreshTokenResponseSchema(BaseResponseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"  # noqa: S105
    user: UserSchema
