from flask import request, jsonify
from flask_classful import FlaskView
from mongoengine import DoesNotExist
from backend.schemas.user_schema import UserSchema
from backend.models.user import User

user_schema = UserSchema()


class UsersView(FlaskView):
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400

        try:
            data = user_schema.load(json_data)
        except ValueError as err:
            return jsonify(err.messages), 400

        u = User(**data)
        u.save()

        return {'result': True}, 201
