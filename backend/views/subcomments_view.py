from flask_apispec import marshal_with, use_kwargs

from backend.schemas.base_schema import ResponseErrorSchema, ResponseSuccessSchema
from backend.services.subcomment_service import SubCommentCheckService, SubCommentLoadService, SubCommentSaveService, \
    SubCommentUpdateService, SubCommentRemoveService
from backend.views.base_view import BaseView
from backend.schemas.subcomment_schema import SubcommentSchema, SubCommentLoadSchema
from flask import jsonify
from flask_classful import route
from mongoengine import DoesNotExist
from backend.views.decorators import token_required
from functools import wraps


def authorization_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sub_comment_id = kwargs['subcomment_id']
        auth_token = kwargs['auth_token']

        if not SubCommentCheckService.is_writer(sub_comment_id, auth_token.user.id):
            return jsonify({'message': 'not authorized'}), 403

        return func(*args, **kwargs)

    return wrapper


class SubcommentsView(BaseView):

    @route('/')
    @marshal_with(SubcommentSchema(many=True), code=200)
    def comments(self, comment_id):
        return SubCommentLoadService.get_many(comment_id)

    @token_required
    @use_kwargs(SubCommentLoadSchema)
    @route('/', methods=['POST'])
    @marshal_with(ResponseSuccessSchema, code=201)
    @marshal_with(ResponseErrorSchema, code=404)
    def post(self, auth_token, comment_id, content):
        result = SubCommentSaveService.post(content, comment_id, auth_token.user)

        if not result:
            return None, 404

        return None, 201

    @route('/<subcomment_id>')
    @marshal_with(SubcommentSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def get(self, subcomment_id, **kwargs):
        try:
            return SubCommentLoadService.get_one(subcomment_id)
        except DoesNotExist:
            return None, 404

    @token_required
    @authorization_required
    @use_kwargs(SubCommentLoadSchema)
    @route('/<string:subcomment_id>', methods=['PUT'])
    @marshal_with(ResponseSuccessSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def put(self, content, subcomment_id, **kwargs):
        result = SubCommentUpdateService.update(subcomment_id, content)

        if not result:
            return None, 404

        return None

    @token_required
    @authorization_required
    @route('/<subcomment_id>', methods=['DELETE'])
    @marshal_with(ResponseSuccessSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def delete(self, comment_id, subcomment_id, **kwargs):
        result = SubCommentRemoveService.delete(comment_id, subcomment_id)

        if not result:
            return None, 404

        return None
