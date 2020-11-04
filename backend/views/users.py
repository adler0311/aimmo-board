from flask import g
from flask_apispec import use_kwargs, marshal_with

from backend.models.comment import Comment
from backend.models.post import Post
from backend.schemas.auth import AuthMarshalSchema
from backend.schemas.post import PostSchema
from backend.schemas.comment import CommentSchema
from flask_classful import FlaskView, route
from backend.schemas.user import UserLoadSchema, UserBodyLoadSchema
from backend.services.user import UserSaveService, UserContentsLoadService
from backend.shared.user_post_type import UserPostType
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
    @marshal_with(PostSchema(many=True), code=200)
    def get_user_posts(self, content_type, **kwargs):
        user_id = g.user.id
        if content_type == UserPostType.WRITE.value:
            return Post.objects(writer=user_id)
        elif content_type == UserPostType.LIKE.value:
            return UserContentsLoadService.get_liked_posts(user_id=user_id)

        return None

    @token_required
    @route('/comments')
    @marshal_with(CommentSchema(many=True), code=200)
    def get_user_comments(self):
        return Comment.objects(writer=g.user.id)
