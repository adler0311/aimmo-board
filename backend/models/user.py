from mongoengine import *
from backend.models.comment import Comment


class User(Document):
    user_id = StringField(db_field='userId')
    password = StringField()
