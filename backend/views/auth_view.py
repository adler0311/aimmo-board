from backend.models.auth_token import AuthToken
from flask import request, jsonify
from flask_classful import FlaskView
from backend.schemas.user_schema import UserSchema
from marshmallow import ValidationError
from backend.services.auth_service import AuthService
from backend.views.decorators import input_data_required, token_required

user_schema = UserSchema()
user_response_schema = UserSchema(only=['user_id', '_id'])
auth_service = AuthService()


class AuthView(FlaskView):

    @input_data_required
    def post(self, **kwargs):
        json_data = kwargs['json_data']

        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return jsonify(err.messages), 400

        token, u = auth_service.sign_in(data)

        if u is None:
            return jsonify({'message': 'user not exist'}), 404

        return {'token': token, 'user': user_response_schema.dump(u)}, 201

    @token_required
    def get(self, **kwargs):
        auth_token: AuthToken = kwargs['auth_token']
        return {'token': auth_token.token, 'user': user_response_schema.dump(auth_token.user)}, 200
