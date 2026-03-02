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
from app.presentation.api.schemas.auth.requests import (
    RefreshTokenRequestSchema,
    RegisterUserRequestSchema,
)
from app.presentation.api.schemas.auth.responses import (
    LoginUserResponseSchema,
    RefreshTokenResponseSchema,
    RegisterUserResponseSchema,
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
    request: RegisterUserRequestSchema,
    interactor: FromDishka[RegisterUser],
) -> RegisterUserResponseSchema:
    response_dto: RegisterUserResponse = await interactor.execute(request)
    return RegisterUserResponseSchema.model_validate(response_dto)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login(
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    interactor: FromDishka[LoginUser],
) -> LoginUserResponseSchema:
    request_dto: LoginUserRequest = LoginUserRequest(
        username=request.username, password=request.password
    )
    response_dto: LoginUserResponse = await interactor.execute(request_dto)
    return LoginUserResponseSchema.model_validate(response_dto)


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
)
async def refresh_token(
    request: RefreshTokenRequestSchema,
    interactor: FromDishka[RefreshToken],
) -> RefreshTokenResponseSchema:
    response_dto: RefreshTokenResponse = await interactor.execute(request)
    return RefreshTokenResponseSchema.model_validate(response_dto)
