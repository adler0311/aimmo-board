from marshmallow import Schema, fields, validate
from backend.schemas.user import UserMarshalSchema
from backend.shared.comments_order_type import CommentsOrderType


class CommentGetSchema(Schema):
    id = fields.String()
    content = fields.String(required=True)
    writer = fields.Nested(UserMarshalSchema)
    post_id = fields.String(required=False)
    created = fields.String()
    likes = fields.Integer()


class CommentLoadSchema(Schema):
    content = fields.String(required=True)


class CommentsLoadSchema(Schema):
    order_type = fields.String(validate=validate.OneOf(CommentsOrderType.list()), data_key='orderType', missing='recent')
    limit = fields.Integer(missing=10, validate=validate.Range(min=1))
    page = fields.Integer(missing=1, validate=validate.Range(min=1))


class CommentSchema(Schema):
    id = fields.String()
    content = fields.String(required=True)
    user_id = fields.String(data_key='userId')
    created = fields.String()
    likes = fields.Integer()
    sub_comments = fields.Integer()


class CommentsSchema(Schema):
    count = fields.Integer()
    comments = fields.Nested(CommentSchema(many=True))
