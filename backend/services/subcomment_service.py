from mongoengine.errors import DoesNotExist
from backend.models.subcomment import Subcomment
from backend.models.comment import Comment
from backend.models.user import User
from bson import ObjectId


class SubcommentService:
    def post(self, data, comment_id, user: User) -> bool:
        try:
            c = Comment.objects.get(id=comment_id)
            sc = Subcomment(**data, parent_id=comment_id, writer=user)
            sc.save()

            Comment.objects(id=c.id).update_one(
                subcomments=[sc] + c.subcomments)
            return True
        except DoesNotExist:
            return False

    def delete(self, comment_id, subcomment_id):
        result = Subcomment.objects(id=subcomment_id).delete()
        if not result:
            return False

        try:
            c = Comment.objects.get(id=comment_id)
            Comment.objects(id=c.id).update_one(subcomments=list(
                filter(lambda c: c.id != ObjectId(subcomment_id), c.subcomments)))
            return True
        except DoesNotExist:
            return False

    def update(self, subcomment_id, content):
        return Subcomment.objects(id=subcomment_id).update_one(
            content=content)

    def get_one(self, subcomment_id):
        return Subcomment.objects.get(id=subcomment_id)

    def get_many(self, comment_id):
        return Subcomment.objects(parent_id=comment_id)

    def is_writer(self, subcomment_id, auth_token_user_id):
        subcomment = Subcomment.objects.get(id=subcomment_id)

        return subcomment.writer.id == auth_token_user_id
