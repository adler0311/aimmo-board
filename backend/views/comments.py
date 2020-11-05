from flask import g
from flask_apispec import use_kwargs, marshal_with
from mongoengine import QuerySet

from backend.models.subcomment import SubComment
from backend.schemas.base import ResponseErrorSchema, ResponseSuccessSchema
from backend.utils import Utils
from backend.views.base import BaseView
from flask_classful import route
from backend.models.comment import Comment
from backend.schemas.comment import CommentGetSchema, CommentsLoadSchema, CommentLoadSchema, CommentsSchema
from backend.views.decorators import token_required


class CommentsView(BaseView):

    @use_kwargs(CommentsLoadSchema, location='query')
    @route('/')
    @marshal_with(CommentsSchema, code=200)
    def index(self, board_id, post_id, order_type, page, limit):
        queryset: QuerySet = Comment.objects(post=post_id)
        start, end = Utils.page_limit_to_start_end(page, limit)
        ordered_comments = Comment.order_by_type(queryset, order_type)[start:end]
        for comment in ordered_comments:
            comment.user_id = comment.writer.user_id
            comment.sub_comments = SubComment.get_count_of_comment(comment.id)

        return {'count': queryset.count(), 'comments': ordered_comments}

    @route('/<string:comment_id>', methods=['GET'])
    @marshal_with(CommentGetSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def get(self, comment_id, **kwargs):
        return Comment.objects.get(id=comment_id)

    @token_required
    @use_kwargs(CommentLoadSchema)
    @route('/', methods=['POST'])
    @marshal_with(ResponseSuccessSchema, code=201)
    @marshal_with(ResponseErrorSchema, code=404)
    def post(self, post_id, content, **kwargs):
        Comment.save_comment(post_id, g.user, content)
        return None, 201

    @token_required
    @use_kwargs(CommentLoadSchema)
    @route('/<string:comment_id>', methods=['PUT'])
    @marshal_with(ResponseSuccessSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def put(self, comment_id, content, **kwargs):
        result = Comment.modify_comment(comment_id, content, g.user)
        if not result:
            return None, 404
        return None, 200

    @token_required
    @route('/<string:comment_id>', methods=['DELETE'])
    @marshal_with(ResponseSuccessSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def delete(self, post_id, comment_id, **kwargs):
        Comment.delete_comment(post_id, comment_id, g.user)
        return None, 200
