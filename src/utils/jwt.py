from jose import JWTError, jwt as jwt_module
from datetime import datetime, timedelta
from typing import Callable, Annotated
from enum import Enum
from fastapi import HTTPException
from utils.shortcuts import get_object_or_none
from models.auth import User


class TokenType(str, Enum):
    Refresh = "refresh"
    Access = "access"


def create_access_token(to_encode: dict, expires_minutes: int, secret_key: str, algorithm: str):
    expires_at = datetime.utcnow() + timedelta(minutes=expires_minutes)

    to_encode.update({"exp": expires_at})
    to_encode.update({"token_type": TokenType.Access})
    encoded_jwt = jwt_module.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def create_refresh_token(to_encode: dict, expires_days: int, secret_key: str, algorithm: str):
    expires_at = datetime.utcnow() + timedelta(days=expires_days)

    to_encode.update({"exp": expires_at})
    to_encode.update({"token_type": TokenType.Refresh})
    encoded_jwt = jwt_module.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def decode_jwt_token(token: str, secret_key: str, algorithm: str):
    payload = jwt_module.decode(token, secret_key, algorithms=[algorithm])
    expiration_timestamp = payload.get("exp")

    if expiration_timestamp:
        current_timestamp = datetime.utcnow().timestamp()
        if current_timestamp > expiration_timestamp:
            return None  # if the token has been expired

    # if there were no expiration time specified for it (special token)
    return payload
