from marshmallow import Schema, fields, validate


class UserBodyLoadSchema(Schema):
    user_id = fields.String(data_key="userId", required=True)
    password = fields.String(data_key="password", required=True)


class UserLoadSchema(Schema):
    content_type = fields.String(validate=validate.OneOf(['write', 'like']), required=True, data_key="type")


class UserMarshalSchema(Schema):
    _id = fields.Function(lambda u: str(u.pk))
    user_id = fields.Str(data_key="userId")
