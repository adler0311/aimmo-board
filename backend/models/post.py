from backend.models.content import Content
from mongoengine import StringField, ListField, ReferenceField
from mongoengine.base.fields import ObjectIdField
from backend.models.comment import Comment


class Post(Content):
    title = StringField()
    board_id = ObjectIdField('boardId')
    comments = ListField(ReferenceField(Comment))
