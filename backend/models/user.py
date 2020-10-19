from mongoengine import *


class User(Document):
    user_id = StringField(db_field='userId')
    password = StringField()
