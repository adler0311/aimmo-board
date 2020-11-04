from flask import g
from flask_apispec import marshal_with, use_kwargs
from flask_classful import route

from backend.models.post import Post
from backend.schemas.base import ResponseSuccessSchema, ResponseErrorSchema
from backend.schemas.post import PostBodyLoadSchema, PostLoadSchema, PostSchema
from backend.services.post import PostLoadService
from backend.views.base import BaseView
from backend.views.decorators import token_required


class PostsView(BaseView):
    @use_kwargs(PostLoadSchema, location='query')
    @route('/')
    @marshal_with(PostSchema(only=['id', 'title', 'content', 'created', 'likes', 'comments'], many=True), code=200)
    def get_board_posts(self, board_id, order_type, limit, is_notice, keyword=None):
        posts = PostLoadService.get_many(board_id=board_id, order_type=order_type, limit=limit, keyword=keyword, is_notice=is_notice)
        return posts, 200

    @token_required
    @use_kwargs(PostBodyLoadSchema)
    @route('', methods=['POST'])
    @marshal_with(ResponseSuccessSchema, code=201)
    @marshal_with(ResponseErrorSchema, code=404)
    def post(self, board_id, title, content):
        Post.save_post(board_id, title, content, g.user)
        return None, 201

    @token_required
    @use_kwargs(PostBodyLoadSchema)
    @route('/<post_id>', methods=['PUT'])
    @marshal_with(ResponseSuccessSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def put(self, board_id, post_id, title, content, **kwargs):
        Post.update_post(board_id, post_id, title, content, g.user)

        return None, 200

    @token_required
    @route('/<post_id>', methods=['DELETE'])
    @marshal_with(ResponseSuccessSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def delete(self, post_id, **kwargs):
        Post.delete_post(post_id, g.user)
        return '', 200
