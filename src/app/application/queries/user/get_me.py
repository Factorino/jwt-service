from typing import TYPE_CHECKING

from app.application.common.dto.base import dto
from app.application.common.dto.user import UserRead
from app.application.interfaces.auth.identity_provider import IIdentityProvider
from app.application.interfaces.common.interactor import Interactor


if TYPE_CHECKING:
    from app.domain.entities.user import User


@dto
class GetMeResponse:
    user: UserRead


class GetMe(Interactor[None, GetMeResponse]):
    def __init__(
        self,
        identity_provider: IIdentityProvider,
    ) -> None:
        self._idp: IIdentityProvider = identity_provider

    async def execute(self, request: None = None) -> GetMeResponse:  # noqa: ARG002
        user: User = await self._idp.get_user()

        return GetMeResponse(
            user=UserRead(
                id=user.id,
                username=user.username,
                role=user.role,
            ),
        )
