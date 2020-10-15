from mongoengine import *


class Comment(Document):
    content = StringField()
    writer = StringField()
    post_id = ObjectIdField('postId')
