from re import sub
from backend.views.base_view import BaseView
from backend.services.subcomment_service import SubcommentService
from backend.schemas.subcomment_schema import SubcommentSchema
from flask import jsonify
from flask_classful import route
from mongoengine import DoesNotExist
from backend.views.decorators import deserialize, input_data_required, token_required
from functools import wraps


subcomments_schema = SubcommentSchema(many=True)
subcomment_schema = SubcommentSchema()
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
    route_base = '/comments/'

    @route('/<comment_id>/subcomments/', methods=['GET'])
    def comments(self, comment_id):
        subcomments = service.get_many(comment_id)
        result = subcomments_schema.dump(subcomments)

        return {'comments': result, 'commentId': comment_id}

    @token_required
    @input_data_required
    @deserialize(subcomment_schema)
    @route('/<comment_id>/subcomments/', methods=['POST'])
    def post_subcomment(self, comment_id, **kwargs):
        auth_token, data = kwargs['auth_token'], kwargs['data']

        result = service.post(data, comment_id, auth_token.user)

        if not result:
            return jsonify({'message': 'Comment matching id does not exist'}), 404

        return {'result': result}, 201

    @route('/<comment_id>/subcomments/<subcomment_id>', methods=['GET'])
    def get(self, comment_id, subcomment_id):
        try:
            subcomment = service.get_one(subcomment_id)

            result = subcomment_schema.dump(subcomment)
            return {'subcomment': result}, 200
        except DoesNotExist:
            return jsonify({'message': 'Post matching query does not exist'}), 404

    @token_required
    @authorization_required
    @input_data_required
    @deserialize(subcomment_schema)
    @route('/<comment_id>/subcomments/<subcomment_id>', methods=['PUT'])
    def put_subcomment(self, comment_id, subcomment_id, **kwargs):
        data = kwargs['data']

        result = service.update(subcomment_id, data['content'])

        if not result:
            return jsonify({'message': 'Comment matching id does not exist'}), 404

        return {'result': True}, 200

    @token_required
    @authorization_required
    @route('/<comment_id>/subcomments/<subcomment_id>/', methods=['DELETE'])
    def delete(self, comment_id, subcomment_id, **kwargs):

        result = service.delete(comment_id, subcomment_id)

        if not result:
            return jsonify({'message': 'id does not exist'}), 404

        return {'result': result}, 200
