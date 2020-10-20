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
