from mongoengine import *
from typing import Dict


class Post(Document):
    _id = ObjectIdField()
    title = StringField()
    content = StringField()
    writer = StringField()
