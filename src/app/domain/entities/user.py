from uuid import UUID

from app.domain.entities.base import Entity, entity
from app.domain.enums.user_role import UserRole


@entity
class User(Entity[UUID]):
    username: str
    password_hash: bytes
    role: UserRole = UserRole.USER
