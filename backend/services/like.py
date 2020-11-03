from backend.models.subcomment import SubComment
from backend.models.comment import Comment
from mongoengine.queryset.visitor import Q
from backend.models.like import Like
from mongoengine.errors import DoesNotExist
from backend.models.post import Post
from backend.models.user import User
from backend.shared.content_type import ContentType


def get_content(content_type):
    if content_type == ContentType.POST.value:
        content = Post
    elif content_type == ContentType.COMMENT.value:
        content = Comment
    elif content_type == ContentType.SUB_COMMENT.value:
        content = SubComment
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
                like = Like(content_id=content_id, user=user.id, content_type=content_type)
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
            like = Like.objects(Q(content_id=content_id) & Q(content_type=content_type) & Q(user=user.id)).first()
            like.update(active=False)

            content = get_content(content_type)
            content = content.objects.get(id=content_id)
            content.update(likes=content.likes - 1 if content.likes is not None else 0)

            return True
        except DoesNotExist:
            return False
