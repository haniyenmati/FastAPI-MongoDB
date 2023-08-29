from passlib.context import CryptContext


class PasswordHash:

    __pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_password_hash(cls, password):
        return cls.__pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.__pwd_context.verify(plain_password, hashed_password)
