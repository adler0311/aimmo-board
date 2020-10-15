from marshmallow import Schema, fields, ValidationError


class UserSchema(Schema):
    _id = fields.Function(lambda u: str(u.pk))
    user_id = fields.Str(data_key="userId")
    password = fields.Str()
