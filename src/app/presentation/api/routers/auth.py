from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.application.commands.auth.login_user import LoginUser, LoginUserRequest, LoginUserResponse
from app.application.commands.auth.refresh_token import (
    RefreshToken,
    RefreshTokenRequest,
    RefreshTokenResponse,
)
from app.application.commands.auth.register_user import (
    RegisterUser,
    RegisterUserRequest,
    RegisterUserResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    route_class=DishkaRoute,
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterUserRequest,
    interactor: FromDishka[RegisterUser],
) -> RegisterUserResponse:
    return await interactor.execute(request)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login(
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    interactor: FromDishka[LoginUser],
) -> LoginUserResponse:
    request_dto: LoginUserRequest = LoginUserRequest(
        username=request.username, password=request.password
    )
    return await interactor.execute(request_dto)


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
)
async def refresh_token(
    request: RefreshTokenRequest,
    interactor: FromDishka[RefreshToken],
) -> RefreshTokenResponse:
    return await interactor.execute(request)
