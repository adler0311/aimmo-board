from backend.views.base_view import BaseView
from backend.models.auth_token import AuthToken
from flask import jsonify
from backend.schemas.user_schema import UserSchema
from backend.services.auth_service import AuthService
from backend.views.decorators import deserialize, input_data_required, token_required

user_schema = UserSchema()
user_response_schema = UserSchema(only=['user_id', '_id'])
auth_service = AuthService()


class AuthView(BaseView):

    @input_data_required
    @deserialize(user_schema)
    def post(self, **kwargs):
        data = kwargs['data']

        token, u = auth_service.sign_in(data)

        if u is None:
            return jsonify({'message': 'user not exist'}), 404

        return {'token': token, 'user': user_response_schema.dump(u)}, 201

    @token_required
    def get(self, **kwargs):
        auth_token: AuthToken = kwargs['auth_token']
        return {'token': auth_token.token, 'user': user_response_schema.dump(auth_token.user)}, 200
