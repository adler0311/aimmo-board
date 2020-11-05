from marshmallow import Schema, fields, EXCLUDE, validate

from backend.schemas.board import BoardSchema
from backend.schemas.user import UserMarshalSchema
from backend.shared.post_order_type import PostOrderType


class PostSchema(Schema):
    id = fields.String()
    title = fields.String(required=True)
    content = fields.String(required=True)
    # writer = fields.Nested(UserMarshalSchema)
    comments = fields.Integer()
    created = fields.String()
    likes = fields.Integer()


class PostLoadSchema(Schema):
    order_type = fields.String(missing=PostOrderType.CREATED.value, validate=validate.OneOf(PostOrderType.list()))
    limit = fields.Int(missing=20)
    keyword = fields.String(missing=None)
    is_notice = fields.Bool(missing=False)


class PostBodyLoadSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.String(required=True)
    content = fields.String(required=True)


class PostDetailsSchema(Schema):
    post = fields.Nested(PostSchema, required=True)
    writer = fields.Nested(UserMarshalSchema, required=True)
    board = fields.Nested(BoardSchema, required=True)


class RecentPostLoadSchema(Schema):
    user_id = fields.String(data_key='userId', required=True)
    limit = fields.Integer(missing=3)


class RecentPostSchema(Schema):
    title = fields.String()
    content = fields.String()


class PopularPostLoadSchema(Schema):
    user_id = fields.String(data_key='userId', required=True)
    limit = fields.Integer(missing=3)


class PopularPostSchema(Schema):
    title = fields.String()
    created = fields.String()
    likes = fields.Integer()


class AdjacentBoardPostLoadSchema(Schema):
    limit = fields.Integer(missing=2)


class AdjacentBoardPostSchema(Schema):
    id = fields.String()
    title = fields.String()
    likes = fields.Integer()
    created = fields.String()
