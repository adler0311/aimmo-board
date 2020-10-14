from mongoengine import *


class Post(Document):
    title = StringField()
    content = StringField()
    writer = StringField()
