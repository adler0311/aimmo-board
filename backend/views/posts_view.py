from enum import Enum
import json
from flask.globals import request
from flask_apispec import marshal_with, use_kwargs

from backend.views.base_view import BaseView
from functools import wraps
from flask import jsonify
from flask_classful import route
from backend.schemas.post_schema import PostLoadSchema, PostSchema
from mongoengine import DoesNotExist
from backend.views.decorators import deserialize, token_required, input_data_required
from backend.services.post_service import PostLoadService, PostService
from distutils.util import strtobool

posts_schema = PostSchema(many=True)
post_schema = PostSchema()
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


def handle_parameters(func):
    @wraps(wrapped=func)
    def wrapper(*args, **kwargs):
        order_type = request.args.get('orderType')
        keyword = request.args.get('keyword')
        limit = request.args.get('limit')
        is_notice = request.args.get('isNotice')

        if is_notice is not None:
            try:
                is_notice = bool(strtobool(is_notice))
            except:
                return jsonify({'message': 'isNotice should be boolean'}), 400
        if order_type is not None and not OrderType.has_value(order_type):
            return jsonify({'message': 'orderType should be one of [created, comments, likes]'}), 400
        if limit is not None and type(limit) is not int:
            return jsonify({'message': 'limit parameter should be int type'}), 400

        kwargs['order_type'] = order_type
        kwargs['keyword'] = keyword
        kwargs['limit'] = limit
        kwargs['is_notice'] = is_notice
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
    @handle_parameters
    @route('/', methods=['GET'])
    def index(self, **kwargs):
        order_type, keyword, limit, is_notice = kwargs['order_type'], kwargs[
            'keyword'], kwargs['limit'], kwargs['is_notice']

        posts = service.get_many(
            order_type, limit, keyword, is_notice=is_notice)

        result = posts_schema.dump(posts)
        return {'posts': result}

    @route('/<string:post_id>', methods=['GET'])
    def get(self, board_id, post_id):
        result, post = service.get_one(post_id)
        if not result:
            return jsonify({'message': 'id does not exist'}), 404

        result = post_schema.dump(post)
        return {'data': result}, 200

    @use_kwargs(PostLoadSchema, location=['query'])
    @route('/boards/<string:board_id>/posts/', methods=['GET'])
    @marshal_with(PostSchema(only=['id'], many=True), code=200)
    def get_board_posts(self, board_id, order_type, keyword, limit, is_notice):
        posts = PostLoadService.get_many(board_id=board_id, order_type=order_type, limit=limit, keyword=keyword, is_notice=is_notice)
        return posts, 200

    @token_required
    @input_data_required
    @deserialize(post_schema)
    @route('/boards/<board_id>/posts/', methods=['POST'])
    def post(self, board_id, **kwargs):
        auth_token, data = kwargs['auth_token'], kwargs['data']

        result = service.post(board_id, data, auth_token.user)
        if not result:
            return jsonify({'message': 'id does not exist'}), 404

        return {'result': True}, 201

    @token_required
    @authorization_required
    @input_data_required
    @deserialize(post_schema)
    @route('/boards/<board_id>/posts/<post_id>/', methods=['PUT'])
    def put(self, board_id, post_id, **kwargs):
        data = kwargs['data']

        result = service.update(board_id, post_id, data)

        if not result:
            return jsonify({'message': 'id does not exist'}), 404

        return {'result': True}, 200

    @token_required
    @authorization_required
    @route('/boards/<board_id>/posts/<post_id>/', methods=['DELETE'])
    def delete(self, board_id, post_id, **kwargs):
        result = service.delete(board_id, post_id)

        if not result:
            return jsonify({'message': 'id does not exist'}), 404

        return {'result': True}, 200
