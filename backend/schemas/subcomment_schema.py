from marshmallow import Schema, fields

from backend.schemas.user_schema import UserMarshalSchema


class SubcommentSchema(Schema):
    _id = fields.Function(lambda c: str(c.pk))
    content = fields.Str(required=True)
    writer = fields.Nested(UserMarshalSchema())
    post_id = fields.Str(required=False)
    parent_id = fields.Str(required=False)
    created = fields.Str()
    likes = fields.Int()


class SubCommentLoadSchema(Schema):
    content = fields.String(required=True)