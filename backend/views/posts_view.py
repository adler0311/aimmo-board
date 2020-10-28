from enum import Enum
from flask_apispec import marshal_with, use_kwargs

from backend.views.base_view import BaseView
from functools import wraps
from flask import jsonify
from flask_classful import route
from backend.schemas.post_schema import PostLoadSchema, PostSchema, PostBodyLoadSchema
from backend.views.decorators import token_required
from backend.services.post_service import PostLoadService, PostService

service = PostService()


def authorization_required(func):
    @wraps(wrapped=func)
    def wrapper(*args, **kwargs):
        post_id = kwargs['post_id']
        auth_token = kwargs['auth_token']

        if not service.is_writer(post_id, auth_token.user.id):
            return jsonify({'message': 'not authorized'}), 403

        return func(*args, **kwargs)

    return wrapper


class OrderType(Enum):
    CREATED = 'created',
    COMMENTS = 'comments',
    LIKES = 'likes',

    @classmethod
    def has_value(cls, value):
        return any(x for x in cls if x.value[0] == value)


class PostsView(BaseView):
    # @handle_parameters
    # @route('/', methods=['GET'])
    # def index(self, **kwargs):
    #     order_type, keyword, limit, is_notice = kwargs['order_type'], kwargs[
    #         'keyword'], kwargs['limit'], kwargs['is_notice']
    #
    #     posts = service.get_many(
    #         order_type, limit, keyword, is_notice=is_notice)
    #
    #     result = posts_schema.dump(posts)
    #     return {'posts': result}

    @use_kwargs(PostLoadSchema, location='query')
    @route('/')
    @marshal_with(PostSchema(only=['_id'], many=True), code=200)
    def get_board_posts(self, board_id, order_type, limit, is_notice, keyword=None):
        posts = PostLoadService.get_many(board_id=board_id, order_type=order_type, limit=limit, keyword=keyword,
                                         is_notice=is_notice)
        return posts, 200

    # @route('/<string:post_id>', methods=['GET'])
    # def get(self, board_id, post_id):
    #     result, post = service.get_one(post_id)
    #     if not result:
    #         return jsonify({'message': 'id does not exist'}), 404
    #
    #     result = post_schema.dump(post)
    #     return {'data': result}, 200
    #
    #
    @token_required
    @use_kwargs(PostBodyLoadSchema)
    @route('/', methods=['POST'])
    def post(self, board_id, auth_token, title, content):
        result = service.post(board_id, title, content, auth_token.user)

        if not result:
            return {'message': 'id does not exist'}, 404

        return {'result': True}, 201

    @token_required
    @authorization_required
    @use_kwargs(PostBodyLoadSchema)
    @route('/<post_id>', methods=['PUT'])
    def put(self, board_id, post_id, title, content, **kwargs):
        result = service.update(board_id, post_id, title, content)

        if not result:
            return {'message': 'id does not exist'}, 404

        return {'result': True}, 200

    @token_required
    @authorization_required
    @route('/<post_id>', methods=['DELETE'])
    def delete(self, board_id, post_id, **kwargs):
        result = service.delete(board_id, post_id)

        if not result:
            return {'message': 'id does not exist'}, 404

        return {'result': True}, 200
