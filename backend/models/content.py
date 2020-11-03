from mongoengine import Document, StringField, ReferenceField, DateTimeField
from mongoengine.fields import IntField
from backend.models.user import User
import datetime

from backend.shared.content_type import ContentType


class Content(Document):
    type = StringField(choices=ContentType.list)
    content = StringField(required=True)
    writer = ReferenceField(document_type=User)
    likes = IntField()
    created = DateTimeField(default=datetime.datetime.now)

    meta = {'abstract': True}
