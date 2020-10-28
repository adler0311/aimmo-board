from marshmallow import Schema, fields


class ResponseErrorSchema(Schema):
    message = fields.String(default="id does not exist")


class ResponseSuccessSchema(Schema):
    result: fields.Boolean(default=True)