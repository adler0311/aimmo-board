from marshmallow import Schema, fields

from backend.schemas.user_schema import UserMarshalSchema


class AuthLoadSchema(Schema):
    token = fields.String(required=True)


class AuthMarshalSchema(Schema):
    token = fields.String()
    user = fields.Nested(UserMarshalSchema(only=['_id', 'user_id']))