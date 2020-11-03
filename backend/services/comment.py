from bson.objectid import ObjectId
from mongoengine.errors import DoesNotExist
from backend.models.comment import Comment
from backend.models.post import Post
from backend.models.user import User


class CommentLoadService:
    @classmethod
    def get_one(cls, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            return comment, True

        except DoesNotExist:
            return None, False


class CommentSaveService:
    @classmethod
    def post(cls, post_id, user: User, content):
        try:
            Post.objects.get(id=post_id)
            comment = Comment(content=content, post=post_id, writer=user)
            comment.save()
            return True
        except DoesNotExist:
            return False


class CommentModifyService:
    @classmethod
    def update(cls, comment_id, content):
        try:
            Comment.objects(id=comment_id).update_one(content=content)
            return True
        except DoesNotExist:
            return False


class CommentRemoveService:
    @classmethod
    def delete(cls, post_id, comment_id):
        try:
            Post.objects.get(id=post_id)
            Comment.objects(id=comment_id).delete()
            return True
        except DoesNotExist:
            return False


class CommentCheckService:
    @classmethod
    def is_writer(cls, comment_id, auth_token_user_id):
        comment = Comment.objects.get(id=comment_id)
        return comment.writer.id == auth_token_user_id
