from backend.models.post import Post
from mongoengine import Document, StringField, DateTimeField
import datetime

from mongoengine.fields import ListField, ReferenceField


class Board(Document):
    title = StringField()
    posts = ListField(ReferenceField(Post))
    created = DateTimeField(default=datetime.datetime.now)
