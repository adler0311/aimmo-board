from mongoengine import Document
from mongoengine.fields import BooleanField, ReferenceField, StringField

from backend.models.user import User
from backend.shared.content_type import ContentType


class Like(Document):
    content_id = StringField(required=True)
    content_type = StringField(choices=ContentType.list())
    user = ReferenceField(document_type=User, required=True)
    active = BooleanField(default=True)
