from models.Auth import User


async def register_user(username: str, password: str) -> User:
    if User.objects(username=username).first():
        return  # TODO raise error that the user with this credentials exists

    user = User(username=username, password=password)
    user.save()
    # TODO return user's data excluding password
    return user._data
