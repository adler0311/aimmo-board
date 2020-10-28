from flask_apispec import use_kwargs, marshal_with

from backend.services.comment_service import CommentService
from backend.views.base_view import BaseView
from flask import jsonify
from flask_classful import route
from backend.models.comment import Comment
from backend.schemas.comment_schema import CommentSchema, CommentLoadSchema
from backend.views.decorators import token_required
from functools import wraps

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

    @route('/')
    @marshal_with(CommentSchema(many=True), 200)
    def comments(self, post_id):
        return Comment.objects(post_id=post_id)

    @token_required
    @route('/', methods=['POST'])
    @use_kwargs(CommentLoadSchema)
    def post(self, post_id, content, auth_token):
        result = service.post(post_id, auth_token.user, content)

        if not result:
            return {'message': 'id does not exist'}, 404

        return {'result': True}, 201

    @route('/<string:comment_id>', methods=['GET'])
    @marshal_with(CommentSchema, 200)
    def get(self, post_id, comment_id):
        comment, result = service.get(comment_id)

        if not result:
            return {'message': 'id does not exist'}, 404

        return comment

    @token_required
    @authorization_required
    @use_kwargs(CommentLoadSchema)
    @route('/<string:comment_id>', methods=['PUT'])
    def put_comment(self, comment_id, content, **kwargs):
        result = service.update(comment_id, content)

        if not result:
            return {'message': 'id does not exist'}, 404

        return {'result': True}, 200

    @token_required
    @authorization_required
    @route('/<string:comment_id>', methods=['DELETE'])
    def delete(self, post_id, comment_id, **kwargs):
        result = service.delete(post_id, comment_id)

        if not result:
            return jsonify({'message': 'id does not exist'}), 404

        return {'result': True}, 200
