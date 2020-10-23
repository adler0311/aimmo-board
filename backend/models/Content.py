from mongoengine import Document, StringField, ReferenceField, DateTimeField
from mongoengine.fields import IntField
from backend.models.user import User
import datetime


class Content(Document):
    type = StringField()
    content = StringField()
    writer = ReferenceField(User)
    likes = IntField()
    created = DateTimeField(default=datetime.datetime.now)

    # meta = {'allow_inheritance': True}
    meta = {'abstract': True}
