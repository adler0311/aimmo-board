from mongoengine import Document, StringField, ReferenceField, DateTimeField
from mongoengine.fields import IntField

from backend.errors import ForbiddenError
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

    def is_writer(self, user):
        return self.writer.id == user.id

    def check_writer(self, user):
        if not self.is_writer(user):
            raise ForbiddenError('작성자가 아닙니다')

    @classmethod
    def increase_like(cls, content_id, content):
        content = content.objects.get(id=content_id)
        content.update(likes=content.likes + 1 if content.likes is not None else 1)

    @classmethod
    def decrease_like(cls, content_id, content):
        content = content.objects.get(id=content_id)
        content.update(likes=content.likes - 1 if content.likes is not None else 0)
