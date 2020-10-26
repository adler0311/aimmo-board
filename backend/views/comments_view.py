from backend.services.comment_service import CommentService
from backend.views.base_view import BaseView
from flask import jsonify
from flask_classful import route
from backend.models.comment import Comment
from backend.schemas.comment_schema import CommentSchema
from backend.views.decorators import deserialize, input_data_required, token_required
from functools import wraps


comments_schema = CommentSchema(many=True)
comment_schema = CommentSchema()
service = CommentService()


def authorization_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        comment_id = kwargs['comment_id']
        auth_token = kwargs['auth_token']

        if not service.is_writer(comment_id, auth_token.user.id):
            return jsonify({'message': 'not authorized'}), 403

        return func(*args, **kwargs)

    return wrapper


class CommentsView(BaseView):
    route_base = '/posts/'

    @route('/<string:post_id>/comments/')
    def comments(self, post_id):
        comments = Comment.objects(post_id=post_id)
        result = comments_schema.dump(comments)
        return {'comments': result, 'postId': post_id}

    @token_required
    @input_data_required
    @deserialize(comment_schema)
    @route('/<post_id>/comments/', methods=['POST'])
    def post_comment(self, post_id, **kwargs):
        auth_token, data = kwargs['auth_token'], kwargs['data']

        result = service.post(post_id, auth_token.user, data)

        if not result:
            return jsonify({'message': 'id does not exist'}), 404

        return {'result': True}, 201

    @route('/<post_id>/comments/<comment_id>', methods=['GET'])
    def get(self, post_id, comment_id):
        comment, result = service.get(comment_id)

        if not result:
            return jsonify({'message': 'id does not exist'}), 404

        return {'comment': comment_schema.dump(comment)}, 200

    @token_required
    @authorization_required
    @input_data_required
    @deserialize(comment_schema)
    @route('/<string:post_id>/comments/<string:comment_id>', methods=['PUT'])
    def put_comment(self, post_id, comment_id, **kwargs):
        data = kwargs['data']

        result = service.update(comment_id, data)

        if not result:
            return jsonify({'message': 'id does not exist'}), 404

        return {'result': True}, 200

    @token_required
    @authorization_required
    @route('/<string:post_id>/comments/<string:comment_id>/', methods=['DELETE'])
    def delete(self, post_id, comment_id, **kwargs):
        result = service.delete(post_id, comment_id)

        if not result:
            return jsonify({'message': 'id does not exist'}), 404

        return {'result': True}, 200
