from backend.models.subcomment import Subcomment
from mongoengine import Document, StringField, ReferenceField, ObjectIdField, DateTimeField
from mongoengine.fields import IntField, ListField
from backend.models.user import User
import datetime


class Comment(Document):
    content = StringField()
    writer = ReferenceField(User)
    post_id = ObjectIdField('postId')
    created = DateTimeField(default=datetime.datetime.now)
    subcomments = ListField(ReferenceField(Subcomment))
    likes = IntField()
