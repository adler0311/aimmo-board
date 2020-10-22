from mongoengine import Document
from mongoengine.base.fields import ObjectIdField
from mongoengine.fields import BooleanField, StringField


class Like(Document):
    content_id = ObjectIdField('contentId')
    content_type = StringField()
    user_id = ObjectIdField('userId')
    active = BooleanField(default=True)
