from flask_apispec import use_kwargs, marshal_with
from flask_classful import route

from backend.schemas.auth_schema import AuthMarshalSchema, AuthLoadSchema
from backend.schemas.base_schema import ResponseErrorSchema
from backend.services.auth_service import AuthLoadService, AuthTokenLoadService
from backend.views.base_view import BaseView
from backend.schemas.user_schema import UserLoadSchema


class AuthView(BaseView):

    @use_kwargs(AuthLoadSchema)
    @marshal_with(AuthMarshalSchema, code=200)
    def get(self, token):
        return AuthTokenLoadService.get_auth_token(token)

    @use_kwargs(UserLoadSchema)
    @route('/', methods=['POST'])
    @marshal_with(AuthMarshalSchema(only=['token', 'user']), code=201)
    @marshal_with(ResponseErrorSchema, code=404)
    def post(self, user_id, password):
        result = AuthLoadService.sign_in(user_id, password)

        if result is None:
            return None, 404

        return result, 201

