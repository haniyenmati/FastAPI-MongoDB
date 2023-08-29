from jose import JWTError, jwt
from models.Auth import User, get_user
from utils import env
from utils.password_hash import PasswordHash


sec_env = env.load_env(env.EnvFields.Security)


SECRET_KEY = sec_env.get("SEC_SECRET_KEY")
ALGORITHM = sec_env.get("SEC_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    sec_env.get("SEC_ACCESS_TOKEN_EXPIRE_MINUTES"))


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def register_controller(username: str, password: str) -> User:
    user_exists = await get_user(username)
    if user_exists:
        # TODO raise error that the user with this credentials exists
        return {"msg": "user exists"}

    hashed_password = PasswordHash.get_password_hash(password)
    user = User(username=username, password=hashed_password)
    user.save()
    # TODO return user's data excluding password
    return user._data


async def login_controller(username: str, password: str):
    user = await get_user(username)

    if not user:
        # TODO raise appropriate error message
        return

    hashed_passwored = user._data.get('password')
    if PasswordHash.verify_password(password, hashed_passwored):
        # TODO return access token
        return {"msg": "accepted"}
    # TODO raise error for incorrect password
    return {"msg": "not accepted"}
