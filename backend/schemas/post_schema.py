from marshmallow import Schema, fields, ValidationError


class PostSchema(Schema):
    _id = fields.String()
    title = fields.Str()
    content = fields.Str()
    writer = fields.Str()
