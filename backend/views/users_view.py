from enum import Enum
from backend.schemas.post_schema import PostSchema
from backend.schemas.comment_schema import CommentSchema
from flask_classful import FlaskView, route, request
from backend.schemas.user_schema import UserSchema
from backend.views.decorators import deserialize, input_data_required, token_required
from backend.services.user_service import UserService
from flask import jsonify


user_schema = UserSchema()
user_response = UserSchema(only=['user_id', '_id'])
service = UserService()

posts_response = PostSchema(exclude=['comments'], many=True)
comments_repsonse = CommentSchema(exclude=['subcomments'], many=True)


class ContentType(Enum):
    POST = 'post',
    COMMENT = 'comment',
    LIKE_POST = 'likePost',

    @classmethod
    def has_value(cls, value):
        return any(x for x in cls if x.value[0] == value)


class UsersView(FlaskView):

    @input_data_required
    @deserialize(user_schema)
    def post(self, **kwargs):
        data = kwargs['data']

        token, user = service.signup(data)

        return {'token': token, 'user': user_response.dump(user)}, 201

    @token_required
    @route('/contents/')
    def get_contents(self, **kwargs):
        auth_token = kwargs['auth_token']
        type = request.args.get('type')
        if type is None:
            return jsonify({'message': '"type" parameter required'}), 400
        if type is not None and not ContentType.has_value(type):
            return jsonify({'message': '"type" parameter shoud be one of ["post", "comment", "likePost"]'}), 400

        result = service.get_user_contents(type, auth_token.user)

        contents = None
        if type == 'post' or type == 'likePost':
            contents = posts_response.dump(result)
        else:
            contents = comments_repsonse.dump(result)

        return {'type': type, 'contents': contents}
