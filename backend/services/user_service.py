from backend.models.like import Like
from backend.models.post import Post
from backend.models.comment import Comment
from backend.models.user import User
from backend.utils import Utils
from backend.models.auth_token import AuthToken


class UserService:
    def signup(self, data):
        data['password'] = Utils.encrypt_password(data['password'])
        u = User(**data)
        u.save()

        token = Utils.generate_token()
        a = AuthToken(token=token, user=u)
        a.save()

        return token, u

    def get_user_contents(self, type, user: User):

        if type == 'post':
            return Post.objects(writer=user.id)
        elif type == 'comment':
            return Comment.objects(writer=user.id)
        else:
            content_ids = list(
                map(lambda l: l.content_id, Like.objects(user_id=user.id)))
            return Post.objects(id__in=content_ids)
