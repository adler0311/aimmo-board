from backend.models.post import Post
from mongoengine import Document, StringField

from mongoengine.fields import ListField, ReferenceField


class Board(Document):
    title = StringField()
    posts = ListField(ReferenceField(Post))
