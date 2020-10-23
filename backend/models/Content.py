from mongoengine import Document, StringField, ReferenceField, ObjectIdField, DateTimeField
from mongoengine.fields import IntField, ListField
from backend.models.user import User
import datetime


class Content(Document):
    type = StringField()
    content = StringField()
    writer = ReferenceField(User)
    likes = IntField()
    created = DateTimeField(default=datetime.datetime.now)

    meta = {'allow_inheritance': True}
