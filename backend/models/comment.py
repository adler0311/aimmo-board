from mongoengine import *
from backend.models.user import User


class Comment(Document):
    content = StringField()
    writer = ReferenceField(User)
    post_id = ObjectIdField('postId')
