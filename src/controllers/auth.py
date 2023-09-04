from jose import JWTError
from datetime import datetime
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi import status
from typing import Annotated
from models.auth import User
from utils import env, password_hash, jwt
from utils.shortcuts import get_object_or_none


sec_env = env.load_env(env.EnvFields.Security)


ACCESS_SECRET_KEY = sec_env.get("SEC_ACCESS_SECRET_KEY")
REFRESH_SECRET_KEY = sec_env.get("SEC_REFRESH_SECRET_KEY")
ALGORITHM = sec_env.get("SEC_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    sec_env.get("SEC_ACCESS_TOKEN_EXPIRE_MINUTES"))
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    sec_env.get("SEC_REFRESH_TOKEN_EXPIRE_DAYS"))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def register_controller(username: str, password: str):
    user_exists = await get_object_or_none(User, username=username)

    if user_exists:
        raise HTTPException(status.HTTP_409_CONFLICT, "user already exists")

    hashed_password = password_hash.get_password_hash(password)
    user = User(username=username, password=hashed_password,
                created_at=datetime.utcnow())
    user.save()

    to_encode = {"sub": user.username}

    access_token = jwt.create_access_token(to_encode,
                                           ACCESS_TOKEN_EXPIRE_MINUTES, ACCESS_SECRET_KEY, ALGORITHM)
    refersh_token = jwt.create_refresh_token(to_encode,
                                             ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_SECRET_KEY, ALGORITHM)

    return {**user._data, "tokens": {"access_token": access_token, "refresh_token": refersh_token}}


async def login_controller(username: str, password: str):
    user = await get_object_or_none(User, username=username)

    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid username")

    hashed_password = user._data.get('password')
    password_is_verified = password_hash.verify_password(
        password, hashed_password)

    if not password_is_verified:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "incorrect password")

    to_encode = {"sub": user.username}

    access_token = jwt.create_access_token(to_encode,
                                           ACCESS_TOKEN_EXPIRE_MINUTES, ACCESS_SECRET_KEY, ALGORITHM)
    refersh_token = jwt.create_refresh_token(to_encode,
                                             ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_SECRET_KEY, ALGORITHM)

    return {"access_token": access_token, "refresh_token": refersh_token}


async def refresh_token_controller(refresh_token: str):
    decoded_data = jwt.decode_jwt_token(
        token=refresh_token, secret_key=REFRESH_SECRET_KEY, algorithm=ALGORITHM)

    expiration_time = decoded_data.get("exp")
    current_timestamp = datetime.utcnow().timestamp()

    if current_timestamp > expiration_time:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "token has been expired")

    to_encode = {"sub": decoded_data.get("sub")}

    access_token = jwt.create_access_token(
        to_encode=to_encode, expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        secret_key=ACCESS_SECRET_KEY, algorithm=ALGORITHM)

    return {"access": access_token}


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode_jwt_token(
            token, ACCESS_SECRET_KEY, algorithm=ALGORITHM)
        username: str = payload.get("sub")

        if not username:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = await get_object_or_none(User, username=username)
    if not user:
        raise credentials_exception
    return user


async def get_token_for_oauth(username: str, password: str):
    raw_answer = await login_controller(username=username, password=password)

    return {"access_token": raw_answer.get("access_token"), "token_type": "bearer"}
