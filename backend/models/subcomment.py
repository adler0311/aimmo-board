from mongoengine import Document, StringField, ReferenceField, ObjectIdField, DateTimeField
from mongoengine.fields import IntField
from backend.models.user import User
import datetime


class Subcomment(Document):
    content = StringField()
    writer = ReferenceField(User)
    post_id = ObjectIdField('postId')
    parent_id = ObjectIdField('parentId')
    created = DateTimeField(default=datetime.datetime.now)
    likes = IntField()
