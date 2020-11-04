from backend.errors import ForbiddenError
from backend.models.content import Content
from mongoengine import ReferenceField

from backend.models.post import Post
from backend.models.user import User


class Comment(Content):
    post = ReferenceField(document_type=Post, required=True)

    @classmethod
    def save_comment(cls, post_id, user: User, content):
        Post.objects.get(id=post_id)
        comment = Comment(content=content, post=post_id, writer=user)
        comment.save()

    @classmethod
    def modify_comment(cls, comment_id, content, user):
        comment = Comment.objects.get(id=comment_id)
        comment.check_writer(user)
        # cls.check_writer(comment, user)
        return comment.update(content=content)

    @classmethod
    def delete_comment(cls, post_id, comment_id, user):
        Post.objects.get(id=post_id)
        comment = Comment.objects.get(id=comment_id)
        comment.check_writer(user)
        cls.check_writer(comment, user)
        comment.delete()

    # @classmethod
    # def check_writer(cls, comment, user: User):
    #     if comment.is_writer(user):
    #         raise ForbiddenError(message="작성자만 삭제가 가능합니다")
