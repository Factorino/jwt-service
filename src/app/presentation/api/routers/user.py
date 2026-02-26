from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Depends, status

from app.application.queries.user.get_by_username import (
    GetUserByUsername,
    GetUserByUsernameRequest,
    GetUserByUsernameResponse,
)
from app.application.queries.user.get_me import GetMe, GetMeResponse
from app.presentation.api.dependencies import get_current_user_token
from app.presentation.api.schemas.mapper import map_to
from app.presentation.api.schemas.user.responses import UserSchema
from typing import Annotated


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
)
async def get_me(
    interactor: FromDishka[GetMe],
    _token: Annotated[str, Depends(get_current_user_token)],
) -> UserSchema:
    response_dto: GetMeResponse = await interactor.execute()
    return map_to(response_dto.user, UserSchema)


@router.get(
    "/{username}",
    status_code=status.HTTP_200_OK,
)
async def get_user_by_username(
    username: str,
    interactor: FromDishka[GetUserByUsername],
    _token: Annotated[str, Depends(get_current_user_token)],
) -> UserSchema:
    request_dto = GetUserByUsernameRequest(username=username)
    response_dto: GetUserByUsernameResponse = await interactor.execute(request_dto)
    return map_to(response_dto.user, UserSchema)
