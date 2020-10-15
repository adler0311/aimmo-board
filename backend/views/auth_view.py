from flask import request, jsonify
from flask_classful import FlaskView, route
from mongoengine import DoesNotExist
from mongoengine.queryset.visitor import Q
from backend.schemas.user_schema import UserSchema
from backend.models.user import User
import secrets
from backend.models.auth_token import AuthToken

user_schema = UserSchema()


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

        token = self.generate_token()
        # todo. 이미 로그인했으면 갱신한다. 따라서 user_id를 같이 저장하는 게 좋다
        a = AuthToken(token=token)
        a.save()

        return {'token': token, 'userId': u.user_id}, 201

    def generate_token(self):
        return secrets.token_urlsafe()
