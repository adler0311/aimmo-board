from backend.schemas.post_schema import PostSchema
from marshmallow import Schema, fields


class BoardSchema(Schema):
    _id = fields.Function(lambda p: str(p.pk))
    title = fields.Str(required=True)
    posts = fields.Nested(PostSchema(many=True))
