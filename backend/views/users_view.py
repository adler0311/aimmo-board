from flask_apispec import use_kwargs, marshal_with

from backend.schemas.auth_schema import AuthMarshalSchema
from backend.schemas.post_schema import PostSchema
from backend.schemas.comment_schema import CommentSchema
from flask_classful import FlaskView, route
from backend.schemas.user_schema import UserLoadSchema, UserBodyLoadSchema
from backend.views.decorators import token_required
from backend.services.user_service import UserService

service = UserService()


class UsersView(FlaskView):

    @use_kwargs(UserBodyLoadSchema)
    @route('', methods=['POST'])
    @marshal_with(AuthMarshalSchema(only=['token', 'user']), 201)
    def post(self, user_id, password):
        auth_token = service.signup(user_id, password)
        return auth_token, 201

    @token_required
    @use_kwargs(UserLoadSchema, location='query')
    @route('/posts')
    @marshal_with(PostSchema(many=True, exclude=['comments']), 200)
    def get_user_posts(self, auth_token, content_type):
        user_id = auth_token.user.id
        if content_type == 'write':
            return service.get_posts(user_id=user_id)
        elif content_type == 'like':
            return service.get_liked_posts(user_id=user_id)

        return None

    @token_required
    @route('/comments')
    @marshal_with(CommentSchema(many=True, exclude=['subcomments']), 200)
    def get_user_comments(self, auth_token):
        return service.get_comments(auth_token.user.id)
