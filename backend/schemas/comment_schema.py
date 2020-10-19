from marshmallow import Schema, fields
from backend.schemas.user_schema import UserSchema


class CommentSchema(Schema):
    _id = fields.Function(lambda c: str(c.pk))
    content = fields.Str()
    writer = fields.Nested(UserSchema(only=['user_id', '_id']))
    post_id = fields.Str()
