from backend.services.subcomment_service import SubcommentService
from backend.schemas.subcomment_schema import SubcommentSchema
from flask import request, jsonify
from flask_classful import FlaskView, route
from backend.models.comment import Comment
from backend.models.post import Post
from backend.schemas.comment_schema import CommentSchema
from mongoengine import DoesNotExist, QuerySet
from bson import ObjectId
from backend.views.decorators import input_data_required, token_required
from functools import wraps
from marshmallow import ValidationError
from backend.models.subcomment import Subcomment

import logging

subcomments_schema = SubcommentSchema(many=True)
subcomment_schema = SubcommentSchema()
subcomment_service = SubcommentService()


def authorization_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        subcomment_id = kwargs['subcomment_id']
        auth_token = kwargs['auth_token']

        qs: QuerySet = Subcomment.objects
        subcomment = qs.get(pk=subcomment_id)

        if subcomment.writer.id != auth_token.user.id:
            return jsonify({'message': 'not authorized'}), 403

        return func(*args, **kwargs)

    return wrapper


# def authorization_required(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         comment_id = kwargs['comment_id']
#         auth_token = kwargs['auth_token']

#         qs: QuerySet = Comment.objects
#         comment = qs.get(pk=comment_id)

#         if comment.writer.id != auth_token.user.id:
#             return jsonify({'message': 'not authorized'}), 403

#         return func(*args, **kwargs)

#     return wrapper


class SubcommentsView(FlaskView):
    route_base = '/comments/'

    @route('/<comment_id>/subcomments/', methods=['GET'])
    def comments(self, comment_id):
        subcomments = Subcomment.objects(parent_id=comment_id)
        result = subcomments_schema.dump(subcomments)
        return {'comments': result, 'commentId': comment_id}

    @token_required
    @input_data_required
    @route('/<comment_id>/subcomments/', methods=['POST'])
    def post_subcomment(self, comment_id, **kwargs):
        auth_token, json_data = kwargs['auth_token'], kwargs['json_data']

        try:
            data = subcomment_schema.load(json_data)
        except ValidationError as err:
            return jsonify(err.messages), 400

        result = subcomment_service.add_subcomment(
            data, comment_id, auth_token.user)

        if not result:
            return jsonify({'message': 'Comment matching id does not exist'}), 404

        return {'result': result}, 201

    # # def get(self, id):
    # #     try:
    # #         post = Post.objects.get(pk=id)
    # #         result = post_schema.dump(post)
    # #         return {'data': result}, 200
    # #     except DoesNotExist as e:
    # #         return jsonify({'message': 'Post matching query does not exist'}), 404

    # 순서는 위에서부터 진행
    @token_required
    @authorization_required
    @input_data_required
    @route('/<comment_id>/subcomments/<subcomment_id>', methods=['PUT'])
    def put_subcomment(self, comment_id, subcomment_id, **kwargs):
        json_data = kwargs['json_data']

        try:
            data = subcomment_schema.load(json_data)
        except ValidationError as err:
            return jsonify(err.messages), 400

        result = Subcomment.objects(pk=subcomment_id).update_one(
            content=data['content'])

        if not result:
            return jsonify({'message': 'Comment matching id does not exist'}), 404

        return {'result': True}, 200

    @token_required
    @authorization_required
    @route('/<comment_id>/subcomments/<subcomment_id>/', methods=['DELETE'])
    def delete(self, comment_id, subcomment_id, **kwargs):

        result = subcomment_service.delete_subcomment(
            comment_id, subcomment_id)

        if not result:
            return jsonify({'message': 'id does not exist'}), 404

        return {'result': result}, 200
