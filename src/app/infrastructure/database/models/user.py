from uuid import UUID

from sqlalchemy import UUID as SA_UUID, Enum, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums.user_role import UserRole
from app.infrastructure.database.models.base import BaseORM


class UserORM(BaseORM):
    __tablename__: str = "users"

    id: Mapped[UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        primary_key=True,
    )

    username: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    password_hash: Mapped[bytes] = mapped_column(
        LargeBinary,
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False,
    )
