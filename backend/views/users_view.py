from flask_classful import FlaskView
from backend.schemas.user_schema import UserSchema
from backend.views.decorators import deserialize, input_data_required
from backend.services.user_service import UserService


user_schema = UserSchema()
user_response = UserSchema(only=['user_id', '_id'])
service = UserService()


class UsersView(FlaskView):

    @input_data_required
    @deserialize(user_schema)
    def post(self, **kwargs):
        data = kwargs['data']

        token, user = service.signup(data)

        return {'token': token, 'user': user_response.dump(user)}, 201
