from flask_apispec import use_kwargs, marshal_with
from flask_classful import route

from backend.schemas.auth_schema import AuthMarshalSchema, AuthLoadSchema
from backend.views.base_view import BaseView
from backend.models.auth_token import AuthToken
from backend.schemas.user_schema import UserLoadSchema
from backend.services.auth_service import AuthService

auth_service = AuthService()


class AuthView(BaseView):

    @use_kwargs(UserLoadSchema)
    @route('/', methods=['POST'])
    @marshal_with(AuthMarshalSchema(only=['token', 'user']), code=201)
    def post(self, user_id, password):
        result = auth_service.sign_in(user_id, password)

        if result is None:
            return {'message': 'id does not exist'}, 404

        return result, 201

    @use_kwargs(AuthLoadSchema)
    @marshal_with(AuthMarshalSchema, code=200)
    def get(self, **kwargs):
        auth_token: AuthToken = kwargs['auth_token']
        return auth_token
