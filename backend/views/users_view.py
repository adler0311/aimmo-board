from flask import request, jsonify
from flask_classful import FlaskView, route
from mongoengine import DoesNotExist
from backend.schemas.user_schema import UserSchema
from backend.models.user import User
from backend.utils import Utils
from backend.models.auth_token import AuthToken
from marshmallow import ValidationError
from backend.views.decorators import input_data_required

user_schema = UserSchema()
user_response = UserSchema(only=['user_id', '_id'])


class UsersView(FlaskView):
    @input_data_required
    def post(self, **kwargs):
        json_data = kwargs['json_data']

        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return jsonify(err.messages), 400

        u = User(**data)
        u.save()

        token = Utils.generate_token()
        a = AuthToken(token=token, user=u)
        a.save()

        return {'token': token, 'user': user_response.dump(u)}, 201
