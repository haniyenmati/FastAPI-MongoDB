from mongoengine import (
    Document, StringField, DateTimeField
)


class User(Document):
    username = StringField(primary_key=True, required=True)
    password = StringField(required=True)


async def get_user(username: str):
    user = User.objects(username=username)

    if user:
        return user.first()
    return None
