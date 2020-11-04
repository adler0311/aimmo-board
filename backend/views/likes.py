from flask import g
from flask_apispec import use_kwargs, marshal_with

from backend.models.like import Like
from backend.schemas.base import ResponseErrorSchema, ResponseSuccessSchema
from backend.views.base import BaseView
from backend.schemas.like import LikeSchema, LikeLoadSchema
from backend.views.decorators import token_required
from flask_classful import route


class LikesView(BaseView):

    @use_kwargs(LikeLoadSchema, location='query')
    @route('/')
    @marshal_with(LikeSchema(many=True), code=200)
    def index(self, content_id, content_type):
        return Like.get_by_content(content_id, content_type)

    @token_required
    @use_kwargs(LikeLoadSchema)
    @route('/', methods=['POST'])
    @marshal_with(ResponseSuccessSchema, code=201)
    @marshal_with(ResponseErrorSchema, code=404)
    def post(self, content_id, content_type):
        Like.activate_like(content_id, content_type, g.user)
        return None, 201

    @token_required
    @use_kwargs(LikeLoadSchema)
    @route('/', methods=['DELETE'])
    @marshal_with(ResponseErrorSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def delete(self, content_id, content_type):
        Like.deactivate_like(content_id, content_type, g.user)
        return None, 200
