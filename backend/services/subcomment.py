from mongoengine.errors import DoesNotExist
from backend.models.subcomment import SubComment
from backend.models.comment import Comment
from backend.models.user import User
from bson import ObjectId


class SubCommentLoadService:

    @classmethod
    def get_many(cls, comment_id):
        return SubComment.objects(parent=comment_id)

    @classmethod
    def get_one(cls, sub_comment_id):
        return SubComment.objects.get(id=sub_comment_id)


class SubCommentSaveService:
    @classmethod
    def post(cls, content, post_id, comment_id, user: User) -> bool:
        try:
            Comment.objects.get(id=comment_id)
            sub_comment = SubComment(content=content, parent=comment_id, writer=user, post=post_id)
            sub_comment.save()

            return True
        except DoesNotExist:
            return False


class SubCommentModifyService:
    @classmethod
    def update(cls, sub_comment_id, content):
        return SubComment.objects(id=sub_comment_id).update_one(content=content)


class SubCommentRemoveService:
    @classmethod
    def delete(cls, comment_id, sub_comment_id):
        try:
            Comment.objects.get(id=comment_id)
            result = SubComment.objects(id=sub_comment_id).delete()
            
            if not result:
                return False
            return True
        except DoesNotExist:
            return False


class SubCommentCheckService:
    @classmethod
    def is_writer(cls, sub_comment_id, auth_token_user_id):
        sub_comment = SubComment.objects.get(id=sub_comment_id)
        return sub_comment.writer.id == auth_token_user_id
