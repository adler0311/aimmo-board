from marshmallow import Schema, fields, validate

from backend.shared.content_type import ContentType


class LikeSchema(Schema):
    id = fields.String()
    user = fields.String(data_key="userId")
    content = fields.String(required=True, data_key="contentId")
    content_type = fields.String(validate=validate.OneOf(ContentType.list()), required=True, data_key="contentType")
    active = fields.Boolean()


class LikeLoadSchema(Schema):
    content_id = fields.String(required=True, data_key="contentId")
    content_type = fields.String(validate=validate.OneOf(ContentType.list()), required=True, data_key="contentType")
