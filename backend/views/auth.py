from flask_apispec import use_kwargs, marshal_with
from flask_classful import route

from backend.schemas.auth import AuthMarshalSchema
from backend.schemas.base import ResponseErrorSchema
from backend.services.auth import AuthLoadService
from backend.views.base import BaseView
from backend.schemas.user import UserBodyLoadSchema
from backend.views.decorators import token_required


class AuthView(BaseView):

    @token_required
    @marshal_with(AuthMarshalSchema, code=200)
    def get(self, **kwargs):
        return kwargs['auth_token']

    @use_kwargs(UserBodyLoadSchema)
    @route('/', methods=['POST'])
    @marshal_with(AuthMarshalSchema(only=['token', 'user']), code=201)
    @marshal_with(ResponseErrorSchema, code=404)
    def post(self, user_id, password):
        result = AuthLoadService.sign_in(user_id, password)

        if result is None:
            return None, 404

        return result, 201
