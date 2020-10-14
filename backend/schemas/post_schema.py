from marshmallow import Schema, fields, ValidationError
from backend.schemas.comment_schema import CommentSchema


class PostSchema(Schema):
    _id = fields.Function(lambda p: str(p.pk))
    title = fields.Str()
    content = fields.Str()
    writer = fields.Str()
    comments = fields.Nested(CommentSchema(many=True))
