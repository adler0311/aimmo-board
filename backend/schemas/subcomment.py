from marshmallow import Schema, fields, validate

from backend.schemas.user import UserMarshalSchema


class SubcommentSchema(Schema):
    id = fields.String()
    content = fields.Str(required=True)
    writer = fields.Nested(UserMarshalSchema())
    post_id = fields.Str(required=False)
    parent_id = fields.Str(required=False)
    created = fields.Str()
    likes = fields.Int()


class SubCommentLoadSchema(Schema):
    content = fields.String(required=True)


class SubCommentsLoadSchema(Schema):
    page = fields.Integer(validate=validate.Range(min=1), missing=1)
    limit = fields.Integer(validate=validate.Range(min=1), missing=10)
