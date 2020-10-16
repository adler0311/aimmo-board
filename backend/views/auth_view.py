from flask import request, jsonify
from flask_classful import FlaskView, route
from mongoengine import DoesNotExist
from mongoengine.queryset.visitor import Q
from backend.schemas.user_schema import UserSchema
from backend.models.user import User
from backend.models.auth_token import AuthToken
from backend.utils import Utils

user_schema = UserSchema()
user_response_schema = UserSchema(only=['user_id', '_id'])


class AuthView(FlaskView):
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400

        try:
            data = user_schema.load(json_data)
        except ValueError as err:
            return jsonify(err.messages), 400

        u = User.objects(Q(user_id=data['user_id']) &
                         Q(password=data['password'])).first()

        if u is None:
            return jsonify({'message': 'user not exist'}), 404

        token = Utils.generate_token()
        a = AuthToken(token=token, user=u)
        a.save()

        return {'token': token, 'user': user_response_schema.dump(u)}, 201
