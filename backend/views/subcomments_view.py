from flask_apispec import marshal_with, use_kwargs

from backend.views.base_view import BaseView
from backend.services.subcomment_service import SubcommentService
from backend.schemas.subcomment_schema import SubcommentSchema, SubCommentLoadSchema
from flask import jsonify
from flask_classful import route
from mongoengine import DoesNotExist
from backend.views.decorators import token_required
from functools import wraps

service = SubcommentService()


def authorization_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        subcomment_id = kwargs['subcomment_id']
        auth_token = kwargs['auth_token']

        if not service.is_writer(subcomment_id, auth_token.user.id):
            return jsonify({'message': 'not authorized'}), 403

        return func(*args, **kwargs)

    return wrapper


class SubcommentsView(BaseView):

    @route('/')
    @marshal_with(SubcommentSchema(many=True), 200)
    def comments(self, comment_id):
        return service.get_many(comment_id)

    @token_required
    @use_kwargs(SubCommentLoadSchema)
    @route('/', methods=['POST'])
    def post(self, auth_token, comment_id, content):
        result = service.post(content, comment_id, auth_token.user)

        if not result:
            return {'message': 'Comment matching id does not exist'}, 404

        return {'result': True}, 201

    @route('/<subcomment_id>')
    @marshal_with(SubcommentSchema, 200)
    def get(self, subcomment_id, **kwargs):
        try:
            return service.get_one(subcomment_id)
        except DoesNotExist:
            return jsonify({'message': 'Post matching query does not exist'}), 404

    @token_required
    @authorization_required
    @use_kwargs(SubCommentLoadSchema)
    @route('/<string:subcomment_id>', methods=['PUT'])
    def put(self, content, subcomment_id, **kwargs):
        result = service.update(subcomment_id, content)

        if not result:
            return {'message': 'Comment matching id does not exist'}, 404

        return {'result': True}, 200

    @token_required
    @authorization_required
    @route('/<subcomment_id>', methods=['DELETE'])
    def delete(self, comment_id, subcomment_id, **kwargs):
        result = service.delete(comment_id, subcomment_id)

        if not result:
            return {'message': 'id does not exist'}, 404

        return {'result': result}, 200
