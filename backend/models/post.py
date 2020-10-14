from mongoengine import *
from backend.models.comment import Comment


class Post(Document):
    title = StringField()
    content = StringField()
    writer = StringField()
    comments = ListField(ReferenceField(Comment))
