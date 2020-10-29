from flask_apispec import use_kwargs, marshal_with

from backend.schemas.base import ResponseErrorSchema, ResponseSuccessSchema
from backend.services.like import LikeLoadService, LikeSaveService, LikeRemoveService
from backend.views.base import BaseView
from backend.schemas.like import LikeSchema, LikeLoadSchema
from backend.views.decorators import token_required
from flask_classful import route


class LikesView(BaseView):

    @use_kwargs(LikeLoadSchema, location='query')
    @route('/')
    @marshal_with(LikeSchema(many=True), code=200)
    def index(self, content_id, content_type):
        return LikeLoadService.get_many(content_id, content_type)

    @token_required
    @use_kwargs(LikeLoadSchema)
    @route('/', methods=['POST'])
    @marshal_with(ResponseSuccessSchema, code=201)
    @marshal_with(ResponseErrorSchema, code=404)
    def post(self, auth_token, content_id, content_type):
        result = LikeSaveService.post(content_id, content_type, auth_token.user)

        if not result:
            return None, 404

        return None, 201

    @token_required
    @use_kwargs(LikeLoadSchema)
    @route('/', methods=['DELETE'])
    @marshal_with(ResponseErrorSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def delete(self, auth_token, content_id, content_type):
        result = LikeRemoveService.delete(content_id, content_type, auth_token.user)

        if not result:
            return None, 404

        return None
