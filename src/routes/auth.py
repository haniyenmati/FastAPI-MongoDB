from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from controllers.auth import (
    register_controller,
    login_controller,
    refresh_token_controller,
    get_current_user,
    get_token_for_oauth
)
from schemas.auth import (
    UserAuthRequest, UserCreationResponse, AuthTokenResponse,
    RefreshTokenRequest, RefreshTokenResponse, OAuthResponse,
    UserRetrieveResponse
)
from models.auth import User


router = APIRouter(
    prefix="/auth",
    tags=["AUTH"],
    dependencies=None
)


@router.post("/register", response_model=UserCreationResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserAuthRequest):
    res = await register_controller(username=user.username,
                                    password=user.password.get_secret_value())
    return res


@router.post("/login", response_model=AuthTokenResponse, status_code=status.HTTP_200_OK)
async def login(user: UserAuthRequest):
    res = await login_controller(username=user.username,
                                 password=user.password.get_secret_value())
    return res


@router.post("/token", response_model=OAuthResponse, status_code=status.HTTP_200_OK)
async def oauth_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    res = await get_token_for_oauth(username=form_data.username, password=form_data.password)
    return res


@router.post("/token/refresh", response_model=RefreshTokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(token: RefreshTokenRequest):
    res = await refresh_token_controller(refresh_token=token.refresh)
    return res


@router.get("/me", response_model=UserRetrieveResponse)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user._data
