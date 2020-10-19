from flask import request, jsonify
from flask_classful import FlaskView, route
from mongoengine import DoesNotExist
from backend.schemas.user_schema import UserSchema
from backend.models.user import User
from backend.utils import Utils
from backend.models.auth_token import AuthToken
from marshmallow import ValidationError

user_schema = UserSchema()
user_response = UserSchema(only=['user_id', '_id'])


class UsersView(FlaskView):
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400

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
