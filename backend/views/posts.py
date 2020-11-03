from functools import wraps

from flask import jsonify
from flask_apispec import marshal_with, use_kwargs
from flask_classful import route
from mongoengine import DoesNotExist

from backend.models.board import Board
from backend.models.post import Post
from backend.schemas.base import ResponseErrorSchema, ResponseSuccessSchema
from backend.schemas.post import PostBodyLoadSchema, PostLoadSchema, PostSchema
from backend.services.post import PostCheckService, PostLoadService, PostModifyService, PostRemoveService, PostSaveService
from backend.views.base import BaseView
from backend.views.decorators import token_required


def authorization_required(func):
    @wraps(wrapped=func)
    def wrapper(*args, **kwargs):
        post_id = kwargs['post_id']
        auth_token = kwargs['auth_token']

        if not PostCheckService.is_writer(post_id, auth_token.user.id):
            return jsonify({'message': 'not authorized'}), 403

        return func(*args, **kwargs)

    return wrapper


def post_exist_check(func):
    @wraps(wrapped=func)
    def wrapper(*args, **kwargs):
        post_id = kwargs['post_id']

        try:
            Post.objects.get(id=post_id)
        except DoesNotExist:
            return jsonify({'message': 'does not exist'}), 404

        return func(*args, **kwargs)

    return wrapper


class PostsView(BaseView):
    @use_kwargs(PostLoadSchema, location='query')
    @route('/')
    @marshal_with(PostSchema(only=['id', 'title', 'content', 'created', 'likes', 'comments'], many=True), code=200)
    def get_board_posts(self, board_id, order_type, limit, is_notice, keyword=None):
        try:
            board = Board.objects.get(id=board_id)
        except DoesNotExist:
            return [], 404

        posts = PostLoadService.get_many(board_id=board.id, order_type=order_type, limit=limit, keyword=keyword, is_notice=is_notice)
        return posts, 200

    @token_required
    @use_kwargs(PostBodyLoadSchema)
    @route('', methods=['POST'])
    @marshal_with(ResponseSuccessSchema, code=201)
    @marshal_with(ResponseErrorSchema, code=404)
    def post(self, board_id, auth_token, title, content):
        PostSaveService.post(board_id, title, content, auth_token.user)
        return None, 201

    @token_required
    @post_exist_check
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
    @post_exist_check
    @authorization_required
    @route('/<post_id>', methods=['DELETE'])
    @marshal_with(ResponseSuccessSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def delete(self, post_id, **kwargs):
        result = PostRemoveService.delete(post_id)

        if not result:
            return None, 404

        return True
