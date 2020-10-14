from marshmallow import Schema, fields


class CommentSchema(Schema):
    _id = fields.Function(lambda c: str(c.pk))
    content = fields.Str()
    writer = fields.Str()
