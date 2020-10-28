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

        return a

    def get_posts(self, user_id):
        return Post.objects(writer=user_id)

    def get_comments(self, user_id):
        return Comment.objects(writer=user_id)

    def get_liked_posts(self, user_id):
        content_ids = list(
            map(lambda l: l.content_id, Like.objects(user_id=user_id)))
        return Post.objects(id__in=content_ids)
