from backend.views.base_view import BaseView
from backend.models.board import Board
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
post_service = PostService()


def authorization_required(func):
    @wraps(wrapped=func)
    def wrapper(*args, **kwargs):
        post_id = kwargs['post_id']
        auth_token = kwargs['auth_token']

        qs: QuerySet = Post.objects
        post = qs.get(pk=post_id)

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
            post = Post.objects.get(pk=post_id)
            result = post_schema.dump(post)
            return {'data': result}, 200
        except DoesNotExist as e:
            return jsonify({'message': 'Post matching query does not exist'}), 404

    @route('/boards/<string:board_id>/posts/', methods=['GET'])
    def get_board_posts(self, board_id):
        try:
            posts = Post.objects(board_id=board_id)
            result = posts_schema.dump(posts)
            return {'posts': result, 'boardId': board_id}, 200
        except DoesNotExist as e:
            return jsonify({'message': 'Posts matching query does not exist'}), 404

    @token_required
    @input_data_required
    @deserialize(post_schema)
    @route('/boards/<board_id>/posts/', methods=['POST'])
    def post(self, board_id, **kwargs):
        auth_token, data = kwargs['auth_token'], kwargs['data']

        try:
            b = Board.objects.get(id=board_id)

            data['writer'] = auth_token.user
            p = Post(**data)
            p.save()

            Board.objects(pk=board_id).update_one(posts=[p] + b.posts)
        except:
            return jsonify({'message': 'board matching id does not exist'}), 404

        return {'result': True}, 201

    @token_required
    @authorization_required
    @input_data_required
    @deserialize(post_schema)
    @route('/boards/<board_id>/posts/<post_id>/', methods=['PUT'])
    def put(self, board_id, post_id, **kwargs):
        data = kwargs['data']

        result = Post.objects(pk=post_id).update_one(
            title=data['title'], content=data['content'])

        if result is None:
            return jsonify({'message': 'Post matching id does not exist'}), 404

        return {'result': True}, 200

    @token_required
    @authorization_required
    @route('/boards/<board_id>/posts/<post_id>/', methods=['DELETE'])
    def delete(self, board_id, post_id, **kwargs):
        result = post_service.delete_post(board_id, post_id)

        if not result:
            return jsonify({'message': 'Post matching id does not exist'}), 404

        return {'result': True}, 200
