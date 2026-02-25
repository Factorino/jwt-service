import uuid

from app.application.common.dto.base import dto
from app.application.common.dto.user import UserRead
from app.application.interfaces.auth.password_hasher import IPasswordHasher
from app.application.interfaces.interactor import Interactor
from app.application.interfaces.transaction_manager import ITransactionManager
from app.application.interfaces.user.user_repository import IUserRepository
from app.domain.entities.user import User
from app.domain.errors.base import AlreadyExistsError, ValidationError


@dto
class RegisterUserRequest:
    username: str
    password: str


@dto
class RegisterUserResponse:
    user: UserRead


class RegisterUser(Interactor[RegisterUserRequest, RegisterUserResponse]):
    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
        uow: ITransactionManager,
    ) -> None:
        self._user_repository: IUserRepository = user_repository
        self._password_hasher: IPasswordHasher = password_hasher
        self._uow: ITransactionManager = uow

    async def execute(self, request: RegisterUserRequest) -> RegisterUserResponse:
        await self._validate(request)

        password_hash: bytes = self._password_hasher.hash_password(request.password)

        user = User(
            id=uuid.uuid4(),
            username=request.username,
            password_hash=password_hash,
        )

        created_user: User = await self._user_repository.add(user)

        try:
            await self._uow.commit()
        except AlreadyExistsError as e:
            raise AlreadyExistsError(
                f"User with username {request.username} already exists"
            ) from e

        return RegisterUserResponse(
            user=UserRead(
                id=created_user.id,
                username=created_user.username,
                role=created_user.role,
            ),
        )

    async def _validate(self, request: RegisterUserRequest) -> None:
        username: str = request.username
        if not username or len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long")

        password: str = request.password
        if not password or len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        existing: User | None = await self._user_repository.find_by_username(username)
        if existing is not None:
            raise AlreadyExistsError(f"User with username '{username}' already exists")
