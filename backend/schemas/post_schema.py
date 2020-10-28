from marshmallow import Schema, fields, EXCLUDE
from backend.schemas.comment_schema import CommentSchema
from backend.schemas.user_schema import UserMarshalSchema


class PostSchema(Schema):
    _id = fields.Function(lambda p: str(p.pk))
    title = fields.String(required=True)
    content = fields.String(required=True)
    writer = fields.Nested(UserMarshalSchema)
    comments = fields.Nested(CommentSchema(many=True))
    created = fields.String()
    likes = fields.Number()


class PostLoadSchema(Schema):
    order_type = fields.String(missing='created')
    limit = fields.Int(missing=20)
    keyword = fields.String(missing=False)
    is_notice = fields.Bool(missing=False)


class PostBodyLoadSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.String(required=True)
    content = fields.String(required=True)