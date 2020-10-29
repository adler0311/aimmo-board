
from marshmallow import Schema, fields


class ResponseErrorSchema(Schema):
    message = fields.Method("generate_error_message")

    def generate_error_message(self, status_code):
        if status_code == 404:
            return "document matching id does not exist"

        NotImplemented


class ResponseSuccessSchema(Schema):
    result = fields.Boolean(default=True)