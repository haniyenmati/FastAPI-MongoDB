from mongoengine import (
    Document, StringField, DateTimeField, UUIDField, ReferenceField, SequenceField
)
from models.auth import User


class Image(Document):
    id = SequenceField(primary_key=True)
    name = StringField(required=True)
    uuid = UUIDField(required=True, unique=True)
    path = StringField(required=True)
    owner = ReferenceField(User, required=True)
    uploaded_at = DateTimeField(required=True)
