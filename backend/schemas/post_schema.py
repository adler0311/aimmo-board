from marshmallow import Schema, fields, ValidationError
from backend.schemas.comment_schema import CommentSchema
from backend.schemas.user_schema import UserSchema


class PostSchema(Schema):
    _id = fields.Function(lambda p: str(p.pk))
    title = fields.Str()
    content = fields.Str()
    writer = fields.Nested(UserSchema(only=['user_id', '_id']))
    comments = fields.Nested(CommentSchema(many=True))
