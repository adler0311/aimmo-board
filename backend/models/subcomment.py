from backend.models.comment import Comment
from backend.models.content import Content
from mongoengine import ReferenceField

from backend.models.post import Post


class SubComment(Content):
    post = ReferenceField(document_type=Post, required=True)
    parent = ReferenceField(document_type=Comment, required=True)
