from mongoengine.fields import BooleanField
from mongoengine.queryset.manager import queryset_manager
from mongoengine.queryset.queryset import QuerySet

from backend.models.board import Board
from backend.models.content import Content
from mongoengine import StringField, ReferenceField

from backend.models.user import User


class Post(Content):
    title = StringField(required=True)
    board = ReferenceField(document_type=Board, required=True)
    is_notice = BooleanField(default=False)

    meta = {'indexes': [
        {'fields': ['$title', '$content']}
    ]}

    @queryset_manager
    def get_posts_with_parameters(self, queryset: QuerySet, order_type, limit, keyword, board_id, is_notice):
        result = queryset.filter(board=board_id)

        if keyword is not None:
            result = result.search_text(keyword)

        if is_notice:
            result = result.filter(is_notice=is_notice)

        result = result.order_by('-' + order_type)
        return result[:limit]

    @classmethod
    def save_post(cls, board_id, title, content, user):
        board: Board = Board.objects.get(id=board_id)
        post = Post(board=board, title=title, content=content, writer=user)
        post.save()

    @classmethod
    def update_post(cls, board_id, post_id, title, content, requester: User):
        board: Board = Board.objects.get(id=board_id)
        post: Post = Post.objects.get(id=post_id)
        post.check_writer(requester)
        post.update(board=board.id, title=title, content=content)

    @classmethod
    def delete_post(cls, post_id, requester):
        post: Post = Post.objects.get(id=post_id)
        post.check_writer(requester)
        post.delete()
