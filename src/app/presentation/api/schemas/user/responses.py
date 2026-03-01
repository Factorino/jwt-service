from uuid import UUID

from app.domain.enums.user_role import UserRole
from app.presentation.api.schemas.common.response import BaseResponseSchema


class UserSchema(BaseResponseSchema):
    id: UUID
    username: str
    role: UserRole
