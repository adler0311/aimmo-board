
from marshmallow import Schema, fields, validate


class LikeSchema(Schema):
    _id = fields.Function(lambda c: str(c.pk))
    user_id = fields.String(data_key="userId")
    content_id = fields.String(required=True, data_key="contentId")
    content_type = fields.String(validate=validate.OneOf(
        ['post', 'comment', 'subcomment']), required=True, data_key="contentType")
    active = fields.Boolean()


class LikeLoadSchema(Schema):
    content_id = fields.String(required=True, data_key="contentId")
    content_type = fields.String(validate=validate.OneOf(
        ['post', 'comment', 'subcomment']), required=True, data_key="contentType")
