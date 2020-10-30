from mongoengine.fields import BooleanField
from mongoengine.queryset.manager import queryset_manager
from mongoengine.queryset.queryset import QuerySet, BaseQuerySet

from backend.models.board import Board
from backend.models.content import Content
from mongoengine import StringField, ReferenceField


class Post(Content):
    title = StringField(required=True)
    board = ReferenceField(document_type=Board, required=True)
    is_notice = BooleanField(default=False)

    meta = {'indexes': [
        {'fields': ['$title', '$content']}
    ]}

    @queryset_manager
    def get_posts_with_parameters(self, queryset: QuerySet, order_type, limit, keyword, board_id, is_notice):
        result: BaseQuerySet = queryset.order_by('-' + order_type)

        if board_id is not None:
            result = result.filter(board=board_id)

        if keyword is not None:
            result = result.search_text(keyword)

        if is_notice:
            result = result.filter(is_notice=is_notice)

        return result[:limit]

