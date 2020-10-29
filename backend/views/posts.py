from flask_apispec import marshal_with, use_kwargs

from backend.schemas.base import ResponseErrorSchema, ResponseSuccessSchema
from backend.views.base import BaseView
from functools import wraps
from flask import jsonify
from flask_classful import route
from backend.schemas.post import PostLoadSchema, PostSchema, PostBodyLoadSchema
from backend.views.decorators import token_required
from backend.services.post import PostLoadService, PostSaveService, PostModifyService, PostRemoveService, PostCheckService


def authorization_required(func):
    @wraps(wrapped=func)
    def wrapper(*args, **kwargs):
        post_id = kwargs['post_id']
        auth_token = kwargs['auth_token']

        if not PostCheckService.is_writer(post_id, auth_token.user.id):
            return jsonify({'message': 'not authorized'}), 403

        return func(*args, **kwargs)

    return wrapper


class PostsView(BaseView):
    @use_kwargs(PostLoadSchema, location='query')
    @route('/')
    @marshal_with(PostSchema(only=['_id'], many=True), code=200)
    def get_board_posts(self, board_id, order_type, limit, is_notice, keyword=None):
        posts = PostLoadService.get_many(board_id=board_id, order_type=order_type, limit=limit, keyword=keyword, is_notice=is_notice)
        return posts

    @token_required
    @use_kwargs(PostBodyLoadSchema)
    @route('', methods=['POST'])
    @marshal_with(ResponseSuccessSchema, code=201)
    @marshal_with(ResponseErrorSchema, code=404)
    def post(self, board_id, auth_token, title, content):
        result = PostSaveService.post(board_id, title, content, auth_token.user)

        if not result:
            return None, 404

        return None, 201

    @token_required
    @authorization_required
    @use_kwargs(PostBodyLoadSchema)
    @route('/<post_id>', methods=['PUT'])
    @marshal_with(ResponseSuccessSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def put(self, board_id, post_id, title, content, **kwargs):
        result = PostModifyService.update(board_id, post_id, title, content)

        if not result:
            return None, 404

        return None

    @token_required
    @authorization_required
    @route('/<post_id>', methods=['DELETE'])
    @marshal_with(ResponseSuccessSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def delete(self, board_id, post_id, **kwargs):
        result = PostRemoveService.delete(board_id, post_id)

        if not result:
            return None, 404

        return None
