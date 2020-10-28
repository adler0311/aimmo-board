from backend.models.user import User
from backend.models.auth_token import AuthToken
from backend.utils import Utils


class AuthLoadService:
    @classmethod
    def sign_in(cls, user_id, password) -> AuthToken:
        encrypted_password = Utils.encrypt_password(password)

        u = User.get_user_by_id_and_password(user_id=user_id, password=encrypted_password)

        if u is None:
            return None

        token = Utils.generate_token()
        auth_token = AuthToken(token=token, user=u)
        auth_token.save()

        return auth_token


class AuthTokenLoadService:
    @classmethod
    def get_auth_token(cls, token):
        return AuthToken.objects.get(token=token)
