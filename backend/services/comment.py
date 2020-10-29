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
            post = Post.objects.get(id=post_id)
            comment = Comment(content=content, post_id=post_id, writer=user)
            comment.save()

            Post.objects(id=post.id).update_one(comments=[comment] + post.comments)
            return True
        except DoesNotExist:
            return False


class CommentModifyService:
    @classmethod
    def update(cls, comment_id, content):
        return Comment.objects(id=comment_id).update_one(content=content)


class CommentRemoveService:
    @classmethod
    def delete(cls, post_id, comment_id):
        try:
            Comment.objects(id=comment_id).delete()
            post = Post.objects.get(id=post_id)
            Post.objects(id=post.id).update_one(comments=list(filter(lambda c: c.id != ObjectId(comment_id), post.comments)))
            return True
        except DoesNotExist:
            return False


class CommentCheckService:
    @classmethod
    def is_writer(cls, comment_id, auth_token_user_id):
        comment = Comment.objects.get(id=comment_id)

        return comment.writer.id == auth_token_user_id
