from marshmallow import Schema, fields
from backend.schemas.user_schema import UserSchema


class SubcommentSchema(Schema):
    _id = fields.Function(lambda c: str(c.pk))
    content = fields.Str(required=True)
    writer = fields.Nested(UserSchema(only=['user_id', '_id']))
    post_id = fields.Str(required=False)
    parent_id = fields.Str(required=False)
    created = fields.Str()
