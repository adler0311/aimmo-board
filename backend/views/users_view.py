from flask import jsonify
from flask_classful import FlaskView
from backend.schemas.user_schema import UserSchema
from marshmallow import ValidationError
from backend.views.decorators import input_data_required
from backend.services.user_sevice import UserService


user_schema = UserSchema()
user_response = UserSchema(only=['user_id', '_id'])
service = UserService()


class UsersView(FlaskView):

    @input_data_required
    def post(self, **kwargs):
        json_data = kwargs['json_data']

        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return jsonify(err.messages), 400

        token, user = service.signup(data)

        return {'token': token, 'user': user_response.dump(user)}, 201
