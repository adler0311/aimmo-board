from marshmallow import Schema, fields
from backend.schemas.comment_schema import CommentSchema
from backend.schemas.user_schema import UserSchema


class PostSchema(Schema):
    _id = fields.Function(lambda p: str(p.pk))
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    writer = fields.Nested(UserSchema(only=['user_id', '_id']))
    comments = fields.Nested(CommentSchema(many=True))
    created = fields.Str()
    likes = fields.Number()


class PostLoadSchema(Schema):
    order_type = fields.String(default='created')
    keyword = fields.String()
    limit = fields.Int(default=20)
    is_notice = fields.Bool(default=False)
