from mongoengine import Document, Q
from mongoengine.fields import BooleanField, ReferenceField, StringField

from backend.models.comment import Comment
from backend.models.content import Content
from backend.models.post import Post
from backend.models.subcomment import SubComment
from backend.models.user import User
from backend.shared.content_type import ContentType


def get_content_model(content_type):
    if content_type == ContentType.POST.value:
        content = Post
    elif content_type == ContentType.COMMENT.value:
        content = Comment
    elif content_type == ContentType.SUB_COMMENT.value:
        content = SubComment
    else:
        content = None

    return content


class Like(Document):
    content_id = StringField(required=True)
    content_type = StringField(choices=ContentType.list())
    user = ReferenceField(document_type=User, required=True)
    active = BooleanField(default=True)

    @classmethod
    def get_by_content(cls, content_id, content_type):
        return Like.objects(Q(content_id=content_id) & Q(content_type=content_type))

    @classmethod
    def activate_like(cls, content_id, content_type, user: User):
        likes = cls.get_by_content(content_id, content_type)

        if len(likes) > 0:
            likes[0].update(active=True)
        else:
            like = Like(content_id=content_id, user=user.id, content_type=content_type)
            like.save()

        Content.increase_like(content_id, get_content_model(content_type))

    @classmethod
    def deactivate_like(cls, content_id, content_type, user):
        like = Like.objects(Q(content_id=content_id) & Q(content_type=content_type) & Q(user=user.id)).get()
        like.update(active=False)

        Content.decrease_like(content_id, get_content_model(content_type))
