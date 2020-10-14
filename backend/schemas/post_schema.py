from marshmallow import Schema, fields, ValidationError


class PostSchema(Schema):
    _id = fields.Function(lambda p: str(p.pk))
    title = fields.Str()
    content = fields.Str()
    writer = fields.Str()
