from marshmallow import Schema, fields, EXCLUDE, validate
from backend.schemas.comment import CommentSchema
from backend.schemas.user import UserMarshalSchema
from backend.shared.post_order_type import PostOrderType


class PostSchema(Schema):
    _id = fields.Function(lambda p: str(p.pk))
    title = fields.String(required=True)
    content = fields.String(required=True)
    writer = fields.Nested(UserMarshalSchema)
    comments = fields.Nested(CommentSchema(many=True))
    created = fields.String()
    likes = fields.Number()


class PostLoadSchema(Schema):
    order_type = fields.String(missing=PostOrderType.CREATED.value, validate=validate.OneOf(PostOrderType))
    limit = fields.Int(missing=20)
    keyword = fields.String(missing=None)
    is_notice = fields.Bool(missing=False)


class PostBodyLoadSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.String(required=True)
    content = fields.String(required=True)
