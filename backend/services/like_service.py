from backend.models.subcomment import Subcomment
from backend.models.comment import Comment
from mongoengine.queryset.visitor import Q
from backend.models.like import Like
from mongoengine.errors import DoesNotExist
from backend.models.post import Post
from backend.models.user import User


class LikeService:
    def get_many(self, content_id: str, content_type: str):
        return Like.objects(Q(content_id=content_id) & Q(content_type=content_type))

    def post(self, data, user: User):
        try:
            content_id, content_type = data['content_id'], data['content_type']
            likes = Like.objects(Q(content_id=content_id) &
                                 Q(content_type=content_type))

            if len(likes) > 0:
                likes[0].update(active=True)
            else:
                like = Like(content_id=content_id, user_id=user.id,
                            content_type=content_type)
                like.save()

            content = self._get_content(content_type)
            c = content.objects.get(id=content_id)

            c.update(likes=c.likes + 1 if c.likes is not None else 1)

            return True
        except DoesNotExist:
            return False

    def delete(self, data, user: User):
        try:
            content_id, content_type = data['content_id'], data['content_type']
            like = Like.objects.get(Q(content_id=content_id) &
                                    Q(content_type=content_type) & Q(user_id=user.id))
            like.update(active=False)

            content = self._get_content(content_type)
            c = content.objects.get(id=content_id)
            c.update(likes=c.likes - 1 if c.likes is not None else 0)

            return True
        except DoesNotExist:
            return False

    def _get_content(self, content_type):
        content = None
        if content_type == 'post':
            content = Post
        elif content_type == 'comment':
            content = Comment
        else:
            content = Subcomment

        return content
