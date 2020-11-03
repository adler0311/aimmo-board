from typing import List

from mongoengine import QuerySet
from mongoengine.errors import DoesNotExist

from backend.errors import ForbiddenError
from backend.models.comment import Comment
from backend.models.user import User
from backend.models.post import Post
from backend.models.board import Board


class PostLoadService:
    @classmethod
    def get_many(cls, order_type=None, limit=None, keyword=None, board_id=None, is_notice=None):
        posts: QuerySet = Post.get_posts_with_parameters(order_type, limit, keyword, board_id, is_notice)
        # for post in posts:
        #     post.comments = Comment.objects(post=post.id).count()
        return posts

    @classmethod
    def get_one(cls, post_id):
        try:
            return True, Post.objects.get(id=post_id)
        except DoesNotExist:
            return False, None


class PostSaveService:
    @classmethod
    def post(cls, board_id, title, content, user: User):
        post = Post(board=board_id, title=title, content=content, writer=user)
        post.save()


class PostModifyService:
    @classmethod
    def update(cls, board_id, post_id, title, content) -> bool:
        try:
            post: Post = Post.objects.get(id=post_id)
            board: Board = Board.objects.get(id=board_id)
            post.update(board=board, title=title, content=content)

            return True
        except DoesNotExist:
            return False


class PostRemoveService:
    @classmethod
    def check_is_writer(cls, post, user):
        if not post.is_writer(user):
            raise ForbiddenError(message='작성자만 삭제가 가능합니다.')

    @classmethod
    def delete(cls, post, requester):
        cls.check_is_writer(post, requester)
        post.delete()


class PostCheckService:
    @classmethod
    def is_writer(cls, post_id, auth_token_user_id) -> bool:
        try:
            post = Post.objects.get(id=post_id)
            return post.writer.id == auth_token_user_id
        except DoesNotExist:
            return False
