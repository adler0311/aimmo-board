from mongoengine.errors import DoesNotExist
from backend.models.subcomment import Subcomment
from backend.models.comment import Comment
from backend.models.user import User
from bson import ObjectId


class SubCommentLoadService:

    @staticmethod
    def get_many(cls, comment_id):
        return Subcomment.objects(parent_id=comment_id)

    @staticmethod
    def get_one(cls, sub_comment_id):
        return Subcomment.objects.get(id=sub_comment_id)


class SubCommentSaveService:
    @staticmethod
    def post(cls, data, comment_id, user: User) -> bool:
        try:
            c = Comment.objects.get(id=comment_id)
            sc = Subcomment(**data, parent_id=comment_id, writer=user)
            sc.save()

            Comment.objects(id=c.id).update_one(
                subcomments=[sc] + c.subcomments)
            return True
        except DoesNotExist:
            return False


class SubCommentUpdateService:
    @staticmethod
    def update(cls, sub_comment_id, content):
        return Subcomment.objects(id=sub_comment_id).update_one(content=content)


class SubCommentRemoveService:
    @staticmethod
    def delete(cls, comment_id, sub_comment_id):
        result = Subcomment.objects(id=sub_comment_id).delete()
        if not result:
            return False

        try:
            comment = Comment.objects.get(id=comment_id)
            Comment.objects(id=comment.id).\
                update_one(subcomments=list(filter(lambda c: c.id != ObjectId(sub_comment_id), comment.subcomments)))

            return True
        except DoesNotExist:
            return False


class SubCommentCheckService:
    @staticmethod
    def is_writer(cls, sub_comment_id, auth_token_user_id):
        sub_comment = Subcomment.objects.get(id=sub_comment_id)
        return sub_comment.writer.id == auth_token_user_id
