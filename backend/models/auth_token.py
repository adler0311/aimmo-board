import datetime
from mongoengine import Document, StringField, ReferenceField, DateTimeField

from backend.models.user import User


class AuthToken(Document):
    token = StringField()
    user = ReferenceField(User)
    created = DateTimeField(default=datetime.datetime.utcnow)
