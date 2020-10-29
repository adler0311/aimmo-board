from mongoengine.errors import DoesNotExist
from backend.models.user import User
from backend.models.post import Post
from backend.models.board import Board


class PostLoadService:
    @classmethod
    def get_many(cls, order_type=None, limit=None, keyword=None, board_id=None, is_notice=None):
        return Post.get_posts_with_parameters(order_type, limit, keyword, board_id, is_notice)

    @classmethod
    def get_one(cls, post_id):
        try:
            return True, Post.objects.get(id=post_id)
        except DoesNotExist:
            return False, None


class PostSaveService:
    @classmethod
    def post(cls, board_id, title, content, user: User) -> bool:
        try:

            post = Post(board_id=board_id, title=title, content=content, writer=user)
            post.save()

            Board.add_post(board_id, post)
            return True
        except DoesNotExist:
            return False


class PostModifyService:
    @classmethod
    def update(cls, board_id, post_id, title, content) -> bool:
        try:
            post: Post = Post.objects.get(id=post_id)
            post.update(board_id=board_id, title=title, content=content)

            if post.board_id != board_id:
                Board.exclude_post(post.board_id, post_id)
                Board.add_post(board_id, post)

            return True
        except DoesNotExist:
            return False


class PostRemoveService:
    @classmethod
    def delete(cls, board_id, post_id):
        result = Post.objects(id=post_id).delete()

        if not result:
            return False

        try:
            board = Board.objects.get(id=board_id)
            Board.exclude_post(board.id, post_id)

            return True
        except DoesNotExist:
            return False


class PostCheckService:
    @classmethod
    def is_writer(cls, post_id, auth_token_user_id):
        post = Post.objects.get(id=post_id)
        return post.writer.id == auth_token_user_id
