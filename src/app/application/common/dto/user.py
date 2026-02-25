from uuid import UUID

from app.application.common.dto.base import dto
from app.domain.enums.user_role import UserRole


@dto
class UserRead:
    id: UUID
    username: str
    role: UserRole
