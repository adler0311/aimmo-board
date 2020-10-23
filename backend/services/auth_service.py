from mongoengine.queryset.visitor import Q
from backend.models.user import User
from backend.models.auth_token import AuthToken
from backend.utils import Utils


class AuthService:
    def sign_in(self, data):
        encrypted_password = Utils.encrypt_password(data['password'])

        u = User.get_user_by_id_and_password(
            user_id=data['user_id'], password=encrypted_password)

        if u is None:
            return None, None

        token = Utils.generate_token()
        a = AuthToken(token=token, user=u)
        a.save()

        return token, u
