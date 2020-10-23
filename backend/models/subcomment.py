from backend.models.content import Content
from mongoengine import ObjectIdField


class Subcomment(Content):
    post_id = ObjectIdField('postId')
    parent_id = ObjectIdField('parentId')
