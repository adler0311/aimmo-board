from mongoengine import Document, StringField


class User(Document):
    user_id = StringField(db_field='userId')
    password = StringField()
