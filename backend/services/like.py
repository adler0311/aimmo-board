from backend.models.subcomment import Subcomment
from backend.models.comment import Comment
from mongoengine.queryset.visitor import Q
from backend.models.like import Like
from mongoengine.errors import DoesNotExist
from backend.models.post import Post
from backend.models.user import User
from backend.shared.like_type import LikeType


def get_content(content_type):
    if content_type == LikeType.POST.value:
        content = Post
    elif content_type == LikeType.COMMENT.value:
        content = Comment
    elif content_type == LikeType.SUB_COMMENT.value:
        content = Subcomment
    else:
        content = None

    return content


class LikeLoadService:
    @classmethod
    def get_many(cls, content_id: str, content_type: str):
        return Like.objects(Q(content_id=content_id) & Q(content_type=content_type))


class LikeSaveService:
    @classmethod
    def post(cls, content_id, content_type, user: User):
        try:
            likes = Like.objects(Q(content_id=content_id) & Q(content_type=content_type))

            if len(likes) > 0:
                likes[0].update(active=True)
            else:
                like = Like(content_id=content_id, user_id=user.id, content_type=content_type)
                like.save()

            content = get_content(content_type)
            content = content.objects.get(id=content_id)

            content.update(likes=content.likes + 1 if content.likes is not None else 1)

            return True
        except DoesNotExist:
            return False


class LikeRemoveService:
    @classmethod
    def delete(cls, content_id, content_type, user: User):
        try:
            like = Like.objects.get(Q(content_id=content_id) & Q(content_type=content_type) & Q(user_id=user.id))
            like.update(active=False)

            content = get_content(content_type)
            content = content.objects.get(id=content_id)
            content.update(likes=content.likes - 1 if content.likes is not None else 0)

            return True
        except DoesNotExist:
            return False
