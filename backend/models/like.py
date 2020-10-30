from mongoengine import Document
from mongoengine.fields import BooleanField, GenericReferenceField, ReferenceField, StringField

from backend.models.user import User


class Like(Document):
    content = GenericReferenceField(required=True)
    content_type = StringField(choices=('post', 'comment', 'sub_comment'))
    user = ReferenceField(document_type=User, required=True)
    active = BooleanField(default=True)
