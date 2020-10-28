from flask_apispec import use_kwargs, marshal_with

from backend.schemas.auth_schema import AuthMarshalSchema
from backend.schemas.post_schema import PostSchema
from backend.schemas.comment_schema import CommentSchema
from flask_classful import FlaskView, route
from backend.schemas.user_schema import UserLoadSchema, UserBodyLoadSchema
from backend.services.user_service import UserSaveService, UserLoadService
from backend.views.decorators import token_required


class UsersView(FlaskView):

    @use_kwargs(UserBodyLoadSchema)
    @route('', methods=['POST'])
    @marshal_with(AuthMarshalSchema(only=['token', 'user']), code=201)
    def post(self, user_id, password):
        auth_token = UserSaveService.signup(user_id, password)
        return auth_token, 201

    @token_required
    @use_kwargs(UserLoadSchema, location='query')
    @route('/posts')
    @marshal_with(PostSchema(many=True, exclude=['comments']), code=200)
    def get_user_posts(self, auth_token, content_type):
        user_id = auth_token.user.id
        if content_type == 'write':
            return UserLoadService.get_posts(user_id=user_id)
        elif content_type == 'like':
            return UserLoadService.get_liked_posts(user_id=user_id)

        return None

    @token_required
    @route('/comments')
    @marshal_with(CommentSchema(many=True, exclude=['subcomments']), code=200)
    def get_user_comments(self, auth_token):
        return UserLoadService.get_comments(auth_token.user.id)
