from flask import g
from flask_apispec import marshal_with, use_kwargs

from backend.models.subcomment import SubComment
from backend.schemas.base import ResponseErrorSchema, ResponseSuccessSchema
from backend.utils import Utils
from backend.views.base import BaseView
from backend.schemas.subcomment import SubcommentSchema, SubCommentLoadSchema, SubCommentsLoadSchema
from flask_classful import route
from backend.views.decorators import token_required


class SubCommentsView(BaseView):

    @use_kwargs(SubCommentsLoadSchema, location='query')
    @route('/')
    @marshal_with(SubcommentSchema(many=True), code=200)
    def index(self, comment_id, page, limit, **kwargs):
        start, end = Utils.page_limit_to_start_end(page, limit)
        return SubComment.objects(parent=comment_id).order_by('-created')[start: end]

    @route('/<string:sub_comment_id>')
    @marshal_with(SubcommentSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def get(self, sub_comment_id, **kwargs):
        sub_comment = SubComment.objects.get(id=sub_comment_id)
        return sub_comment, 200

    @token_required
    @use_kwargs(SubCommentLoadSchema)
    @route('/', methods=['POST'])
    @marshal_with(ResponseSuccessSchema, code=201)
    @marshal_with(ResponseErrorSchema, code=404)
    def post(self, post_id, comment_id, content, **kwargs):
        SubComment.save_sub_comment(content, post_id, comment_id, g.user)
        return None, 201

    @token_required
    @use_kwargs(SubCommentLoadSchema)
    @route('/<string:sub_comment_id>', methods=['PUT'])
    @marshal_with(ResponseSuccessSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def put(self, content, comment_id, sub_comment_id, **kwargs):
        result = SubComment.update_sub_comment(comment_id, sub_comment_id, content, g.user)
        if not result:
            return None, 404

        return None, 200

    @token_required
    @route('/<string:sub_comment_id>', methods=['DELETE'])
    @marshal_with(ResponseSuccessSchema, code=200)
    @marshal_with(ResponseErrorSchema, code=404)
    def delete(self, comment_id, sub_comment_id, **kwargs):
        SubComment.delete_sub_comment(comment_id, sub_comment_id, g.user)

        return None, 200
