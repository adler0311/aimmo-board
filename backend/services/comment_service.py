from typing import Tuple
from bson.objectid import ObjectId
from mongoengine.errors import DoesNotExist
from backend.models.comment import Comment
from backend.models.post import Post
from backend.models.user import User


class CommentLoadService:
    @staticmethod
    def get_one(cls, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            return comment, True

        except DoesNotExist:
            return None, False


class CommentSaveService:
    @staticmethod
    def post(cls, post_id, user: User, content):
        try:
            p = Post.objects.get(id=post_id)
            c = Comment(content=content, post_id=post_id, writer=user)
            c.save()

            Post.objects(id=p.id).update_one(comments=[c] + p.comments)
            return True
        except DoesNotExist:
            return False


class CommentModifyService:
    @staticmethod
    def update(self, comment_id, data):
        return Comment.objects(id=comment_id).update_one(content=data['content'])


class CommentRemoveService:
    @staticmethod
    def delete(cls, post_id, comment_id):
        try:
            Comment.objects(id=comment_id).delete()
            p = Post.objects.get(id=post_id)
            Post.objects(id=p.id).update_one(comments=list(filter(lambda c: c.id != ObjectId(comment_id), p.comments)))
            return True
        except DoesNotExist:
            return False


class CommentCheckService:
    @staticmethod
    def is_writer(cls, comment_id, auth_token_user_id):
        comment = Comment.objects.get(id=comment_id)

        return comment.writer.id == auth_token_user_id
