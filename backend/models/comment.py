from backend.models.content import Content
from backend.models.subcomment import Subcomment
from mongoengine import ReferenceField, ObjectIdField
from mongoengine.fields import ListField


class Comment(Content):
    post_id = ObjectIdField('postId')
    subcomments = ListField(ReferenceField(Subcomment))
