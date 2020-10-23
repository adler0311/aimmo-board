from backend.views.base_view import BaseView
from functools import wraps
from flask import jsonify
from flask_classful import route
from backend.models.post import Post
from backend.schemas.post_schema import PostSchema
from mongoengine import DoesNotExist, QuerySet
from backend.views.decorators import deserialize, token_required, input_data_required
from backend.services.post_service import PostService

posts_schema = PostSchema(many=True)
post_schema = PostSchema()
service = PostService()


def authorization_required(func):
    @wraps(wrapped=func)
    def wrapper(*args, **kwargs):
        post_id = kwargs['post_id']
        auth_token = kwargs['auth_token']

        qs: QuerySet = Post.objects
        post = qs.get(id=post_id)

        if post.writer.id != auth_token.user.id:
            return jsonify({'message': 'not authorized'}), 403

        return func(*args, **kwargs)

    return wrapper


class PostsView(BaseView):
    route_base = '/'

    @route('/posts/', methods=['GET'])
    def index(self):
        posts = Post.objects()
        result = posts_schema.dump(posts)
        return {'posts': result}

    @route('/boards/<board_id>/posts/<post_id>/', methods=['GET'])
    def get(self, board_id, post_id):
        try:
            post = Post.objects.get(id=post_id)
            result = post_schema.dump(post)
            return {'data': result}, 200
        except DoesNotExist as e:
            return jsonify({'message': 'id does not exist'}), 404

    @route('/boards/<string:board_id>/posts/', methods=['GET'])
    def get_board_posts(self, board_id):
        try:
            posts = Post.objects(board_id=board_id)
            result = posts_schema.dump(posts)
            return {'posts': result, 'boardId': board_id}, 200
        except DoesNotExist as e:
            return jsonify({'message': 'id does not exist'}), 404

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

        if result is None:
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
