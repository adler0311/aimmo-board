from mongoengine import Document, StringField


class Board(Document):
    title = StringField(required=True)
