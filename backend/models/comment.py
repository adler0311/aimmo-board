from backend.models.content import Content
from mongoengine import ReferenceField

from backend.models.post import Post


class Comment(Content):
    post = ReferenceField(document_type=Post, required=True)


