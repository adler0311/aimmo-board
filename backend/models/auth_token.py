from mongoengine import *
import datetime

from backend.models.user import User


class AuthToken(Document):
    token = StringField()
    user = ReferenceField(User)
    created = DateTimeField(default=datetime.datetime.utcnow)
