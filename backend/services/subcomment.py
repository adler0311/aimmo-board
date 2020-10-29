from mongoengine.errors import DoesNotExist
from backend.models.subcomment import Subcomment
from backend.models.comment import Comment
from backend.models.user import User
from bson import ObjectId


class SubCommentLoadService:

    @classmethod
    def get_many(cls, comment_id):
        return Subcomment.objects(parent_id=comment_id)

    @classmethod
    def get_one(cls, sub_comment_id):
        return Subcomment.objects.get(id=sub_comment_id)


class SubCommentSaveService:
    @classmethod
    def post(cls, content, comment_id, user: User) -> bool:
        try:
            comment = Comment.objects.get(id=comment_id)
            sub_comment = Subcomment(content=content, parent_id=comment_id, writer=user)
            sub_comment.save()

            Comment.objects(id=comment.id).update_one(subcomments=[sub_comment] + comment.subcomments)
            return True
        except DoesNotExist:
            return False


class SubCommentModifyService:
    @classmethod
    def update(cls, sub_comment_id, content):
        return Subcomment.objects(id=sub_comment_id).update_one(content=content)


class SubCommentRemoveService:
    @classmethod
    def delete(cls, comment_id, sub_comment_id):
        result = Subcomment.objects(id=sub_comment_id).delete()
        if not result:
            return False

        try:
            comment = Comment.objects.get(id=comment_id)
            Comment.objects(id=comment.id).update_one(subcomments=list(filter(lambda c: c.id != ObjectId(sub_comment_id), comment.subcomments)))

            return True
        except DoesNotExist:
            return False


class SubCommentCheckService:
    @classmethod
    def is_writer(cls, sub_comment_id, auth_token_user_id):
        sub_comment = Subcomment.objects.get(id=sub_comment_id)
        return sub_comment.writer.id == auth_token_user_id
