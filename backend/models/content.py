from mongoengine import Document, StringField, ReferenceField, DateTimeField
from mongoengine.fields import IntField
from backend.models.user import User
import datetime


class Content(Document):
    type = StringField(choices=('post', 'comment', 'sub_comment'))
    content = StringField(required=True)
    writer = ReferenceField(document_type=User)
    likes = IntField()
    created = DateTimeField(default=datetime.datetime.now)

    meta = {'abstract': True}
