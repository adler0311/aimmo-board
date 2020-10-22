from backend.models.subcomment import Subcomment
from mongoengine import Document, StringField, ReferenceField, ObjectIdField, DateTimeField
from mongoengine.fields import ListField
from backend.models.user import User
import datetime


class Content(Document):
    type = StringField()
    writer = ReferenceField(User)

    meta = {'allow_inheritance': True}
