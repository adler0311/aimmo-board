from backend.models.user import User
from backend.models.auth_token import AuthToken
from backend.utils import Utils


class AuthService:
    def sign_in(self, user_id, password) -> AuthToken:
        encrypted_password = Utils.encrypt_password(password)

        u = User.get_user_by_id_and_password(
            user_id=user_id, password=encrypted_password)

        if u is None:
            return None

        token = Utils.generate_token()
        a = AuthToken(token=token, user=u)
        a.save()

        return a

    def get_auth_token(self, token):
        return AuthToken.objects.get(token=token)
