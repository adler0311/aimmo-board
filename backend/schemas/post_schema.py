from marshmallow import Schema, fields, ValidationError


class PostSchema(Schema):
    _id = fields.String(required=False)
    title = fields.Str()
    content = fields.Str()
    writer = fields.Str()
