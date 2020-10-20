from flask import jsonify
from mongoengine.queryset.visitor import Q
from backend.models.user import User
from backend.models.auth_token import AuthToken
from backend.utils import Utils


class AuthService:
    def sign_in(self, data):
        u = User.objects(Q(user_id=data['user_id']) &
                         Q(password=data['password'])).first()

        if u is None:
            return None, None

        token = Utils.generate_token()
        a = AuthToken(token=token, user=u)
        a.save()

        return token, u
