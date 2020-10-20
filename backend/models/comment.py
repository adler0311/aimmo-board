from mongoengine import Document, StringField, ReferenceField, ObjectIdField, DateTimeField
from backend.models.user import User
import datetime


class Comment(Document):
    content = StringField()
    writer = ReferenceField(User)
    post_id = ObjectIdField('postId')
    created = DateTimeField(default=datetime.datetime.now)
