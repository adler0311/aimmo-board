from backend.schemas.like_schema import LikeSchema
from marshmallow import Schema, fields, ValidationError
from backend.schemas.comment_schema import CommentSchema
from backend.schemas.user_schema import UserSchema


class PostSchema(Schema):
    _id = fields.Function(lambda p: str(p.pk))
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    writer = fields.Nested(UserSchema(only=['user_id', '_id']))
    comments = fields.Nested(CommentSchema(many=True))
    created = fields.Str()
    # likes = fields.Nested(LikeSchema(many=True))
    likes = fields.Number()
