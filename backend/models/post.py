from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField
from mongoengine.base.fields import ObjectIdField
from backend.models.comment import Comment
from backend.models.user import User
import datetime


class Post(Document):
    title = StringField()
    content = StringField()
    comments = ListField(ReferenceField(Comment))
    writer = ReferenceField(User)
    created = DateTimeField(default=datetime.datetime.now)
    board_id = ObjectIdField('boardId')
