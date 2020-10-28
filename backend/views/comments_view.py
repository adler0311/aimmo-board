from flask_apispec import use_kwargs, marshal_with

from backend.schemas.base_schema import ResponseErrorSchema, ResponseSuccessSchema
from backend.services.comment_service import CommentCheckService, CommentSaveService, CommentLoadService, \
    CommentModifyService, CommentRemoveService
from backend.views.base_view import BaseView
from flask import jsonify
from flask_classful import route
from backend.models.comment import Comment
from backend.schemas.comment_schema import CommentSchema, CommentLoadSchema
from backend.views.decorators import token_required
from functools import wraps


def authorization_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        comment_id = kwargs['comment_id']
        auth_token = kwargs['auth_token']

        if not CommentCheckService.is_writer(comment_id, auth_token.user.id):
            return jsonify({'message': 'not authorized'}), 403

        return func(*args, **kwargs)

    return wrapper


class CommentsView(BaseView):

    @route('/')
    @marshal_with(CommentSchema(many=True), code=200)
    def comments(self, post_id):
        return Comment.objects(post_id=post_id)

    @token_required
    @use_kwargs(CommentLoadSchema)
    @route('/', methods=['POST'])
    @marshal_with(ResponseSuccessSchema, code=201)
    @marshal_with(ResponseErrorSchema, code=404)
    def post(self, post_id, content, auth_token):
        result = CommentSaveService.post(post_id, auth_token.user, content)

        if not result:
            return None, 404

        return None, 201

    @route('/<string:comment_id>', methods=['GET'])
    @marshal_with(CommentSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def get(self, post_id, comment_id):
        comment, result = CommentLoadService.get(comment_id)

        if not result:
            return None, 404

        return comment

    @token_required
    @authorization_required
    @use_kwargs(CommentLoadSchema)
    @route('/<string:comment_id>', methods=['PUT'])
    @marshal_with(ResponseSuccessSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def put_comment(self, comment_id, content, **kwargs):
        result = CommentModifyService.update(comment_id, content)

        if not result:
            return None, 404

        return None

    @token_required
    @authorization_required
    @route('/<string:comment_id>', methods=['DELETE'])
    @marshal_with(ResponseSuccessSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def delete(self, post_id, comment_id, **kwargs):
        result = CommentRemoveService.delete(post_id, comment_id)

        if not result:
            return None, 404

        return None
