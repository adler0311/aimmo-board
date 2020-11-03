from flask_apispec import marshal_with, use_kwargs

from backend.schemas.base import ResponseErrorSchema, ResponseSuccessSchema
from backend.services.subcomment import SubCommentCheckService, SubCommentLoadService, SubCommentSaveService, SubCommentModifyService, SubCommentRemoveService
from backend.views.base import BaseView
from backend.schemas.subcomment import SubcommentSchema, SubCommentLoadSchema
from flask import jsonify
from flask_classful import route
from mongoengine import DoesNotExist
from backend.views.decorators import token_required
from functools import wraps


def authorization_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sub_comment_id = kwargs['sub_comment_id']
        auth_token = kwargs['auth_token']

        try:
            if not SubCommentCheckService.is_writer(sub_comment_id, auth_token.user.id):
                return jsonify({'message': 'not authorized'}), 403
        except DoesNotExist:
            return jsonify(({'message': 'id does not exist'})), 404

        return func(*args, **kwargs)

    return wrapper


class SubCommentsView(BaseView):

    @route('')
    @marshal_with(SubcommentSchema(many=True), code=200)
    def index(self, comment_id, **kwargs):
        return SubCommentLoadService.get_many(comment_id)

    @route('/<string:sub_comment_id>')
    @marshal_with(SubcommentSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def get(self, sub_comment_id, **kwargs):
        try:
            return SubCommentLoadService.get_one(sub_comment_id)
        except DoesNotExist:
            return None, 404

    @token_required
    @use_kwargs(SubCommentLoadSchema)
    @route('', methods=['POST'])
    @marshal_with(ResponseSuccessSchema, code=201)
    @marshal_with(ResponseErrorSchema, code=404)
    def post(self, auth_token, post_id, comment_id, content, **kwargs):
        result = SubCommentSaveService.post(content, post_id, comment_id, auth_token.user)

        if not result:
            return None, 404

        return None, 201

    @token_required
    @authorization_required
    @use_kwargs(SubCommentLoadSchema)
    @route('/<string:sub_comment_id>', methods=['PUT'])
    @marshal_with(ResponseSuccessSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def put(self, content, sub_comment_id, **kwargs):
        result = SubCommentModifyService.update(sub_comment_id, content)

        if not result:
            return None, 404

        return None

    @token_required
    @authorization_required
    @route('/<string:sub_comment_id>', methods=['DELETE'])
    @marshal_with(ResponseSuccessSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def delete(self, comment_id, sub_comment_id, **kwargs):
        result = SubCommentRemoveService.delete(comment_id, sub_comment_id)

        if not result:
            return None, 404

        return None
