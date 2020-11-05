from backend.models.content import Content
from mongoengine import QuerySet, ReferenceField

from backend.models.post import Post
from backend.models.user import User
from backend.shared.comments_order_type import CommentsOrderType


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

    @classmethod
    def order_by_type(cls, queryset: QuerySet, order_type):
        if order_type == CommentsOrderType.BEST.value:
            return queryset.order_by('-likes')
        else:
            return queryset.order_by('-created')
