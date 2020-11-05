from backend.models.comment import Comment
from backend.models.content import Content
from mongoengine import QuerySet, ReferenceField

from backend.models.post import Post


class SubComment(Content):
    post = ReferenceField(document_type=Post, required=True)
    parent = ReferenceField(document_type=Comment, required=True)

    @classmethod
    def save_sub_comment(cls, content, post_id, comment_id, user):
        Comment.objects.get(id=comment_id)
        sub_comment = SubComment(content=content, parent=comment_id, writer=user, post=post_id)
        sub_comment.save()

    @classmethod
    def update_sub_comment(cls, comment_id, sub_comment_id, content, requester):
        Comment.objects.get(id=comment_id)
        sub_comment: SubComment = SubComment.objects.get(id=sub_comment_id)
        sub_comment.check_writer(requester)
        return sub_comment.update(content=content)

    @classmethod
    def delete_sub_comment(cls, comment_id, sub_comment_id, requester):
        Comment.objects.get(id=comment_id)
        sub_comment: SubComment = SubComment.objects.get(id=sub_comment_id)
        sub_comment.check_writer(requester)
        sub_comment.delete()

    @classmethod
    def get_count_of_comment(cls, comment_id):
        queryset: QuerySet = cls.objects(parent=comment_id)
        return queryset.count()
