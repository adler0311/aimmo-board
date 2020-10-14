from mongoengine import *


class Post(Document):
    _id = ObjectIdField(primary_key=True)
    title = StringField()
    content = StringField()
    writer = StringField()
