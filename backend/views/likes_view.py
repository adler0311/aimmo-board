from flask_apispec import use_kwargs, marshal_with

from backend.services.like_service import LikeLoadService, LikeSaveService, LikeRemoveService
from backend.views.base_view import BaseView
from backend.schemas.like_schema import LikeSchema, LikeLoadSchema
from backend.views.decorators import token_required
from flask_classful import route


class LikesView(BaseView):

    @use_kwargs(LikeLoadSchema, location='query')
    @route('/')
    @marshal_with(LikeSchema(many=True), 200)
    def index(self, content_id, content_type):
        return LikeLoadService.get_many(content_id, content_type)

    @token_required
    @use_kwargs(LikeLoadSchema)
    @route('/', methods=['POST'])
    def post(self, auth_token, content_id, content_type):
        result = LikeSaveService.post(content_id, content_type, auth_token.user)

        if not result:
            return {'message': 'id does not exist'}, 404

        return {'result': True}, 201

    @token_required
    @use_kwargs(LikeLoadSchema)
    @route('/', methods=['DELETE'])
    def delete(self, auth_token, content_id, content_type):
        result = LikeRemoveService.delete(content_id, content_type, auth_token.user)

        if not result:
            return {'message': 'id does not exist'}, 404

        return {'result': True}, 200
