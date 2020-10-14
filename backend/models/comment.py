from mongoengine import *


class Comment(Document):
    content = StringField()
    writer = StringField()
