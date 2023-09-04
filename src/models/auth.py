from mongoengine import (
    Document, StringField, DateTimeField
)


class User(Document):
    username = StringField(primary_key=True, required=True)
    password = StringField(required=True)
    created_at = DateTimeField(required=True)
