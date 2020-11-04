from mongoengine import QuerySet

from backend.models.post import Post
from backend.models.board import Board


class PostLoadService:
    @classmethod
    def get_many(cls, order_type=None, limit=None, keyword=None, board_id=None, is_notice=None):
        Board.objects.get(id=board_id)
        posts: QuerySet = Post.get_posts_with_parameters(order_type, limit, keyword, board_id, is_notice)
        # for post in posts:
        #     post.comments = Comment.objects(post=post.id).count()
        return posts
