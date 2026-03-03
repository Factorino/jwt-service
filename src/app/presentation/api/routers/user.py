from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, status

from app.application.common.dto.user import UserRead
from app.application.queries.user.get_by_username import (
    GetUserByUsername,
    GetUserByUsernameRequest,
    GetUserByUsernameResponse,
)
from app.application.queries.user.get_me import GetMe, GetMeResponse
from app.presentation.api.dependencies import get_current_user_token


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    route_class=DishkaRoute,
)


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
)
async def get_me(
    interactor: FromDishka[GetMe],
    _token: Annotated[str, Depends(get_current_user_token)],
) -> UserRead:
    response_dto: GetMeResponse = await interactor.execute()
    return response_dto.user


@router.get(
    "/{username}",
    status_code=status.HTTP_200_OK,
)
async def get_user_by_username(
    username: str,
    interactor: FromDishka[GetUserByUsername],
    _token: Annotated[str, Depends(get_current_user_token)],
) -> UserRead:
    request_dto = GetUserByUsernameRequest(username=username)
    response_dto: GetUserByUsernameResponse = await interactor.execute(request_dto)
    return response_dto.user
