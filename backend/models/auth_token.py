from mongoengine import *
import datetime


class AuthToken(Document):
    token = StringField()
    created = DateTimeField(default=datetime.datetime.utcnow)
