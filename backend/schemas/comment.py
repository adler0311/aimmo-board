from backend.schemas.subcomment import SubcommentSchema
from marshmallow import Schema, fields
from backend.schemas.user import UserMarshalSchema


class CommentSchema(Schema):
    _id = fields.Function(lambda c: str(c.pk))
    content = fields.Str(required=True)
    writer = fields.Nested(UserMarshalSchema)
    post_id = fields.Str(required=False)
    created = fields.Str()
    likes = fields.Number()


class CommentLoadSchema(Schema):
    content = fields.String(required=True)
