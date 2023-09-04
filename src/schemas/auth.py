from pydantic import BaseModel, Field, SecretStr
from datetime import datetime


class UserAuthRequest(BaseModel):
    username: str
    password: SecretStr


class AuthTokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class OAuthResponse(BaseModel):
    access_token: str
    token_type: str


class UserCreationResponse(BaseModel):
    username: str
    created_at: datetime
    tokens: AuthTokenResponse


class UserRetrieveResponse(BaseModel):
    username: str
    created_at: datetime


class RefreshTokenRequest(BaseModel):
    refresh: str


class RefreshTokenResponse(BaseModel):
    access: str
