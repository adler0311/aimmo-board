import secrets
import hashlib


class Utils:
    @staticmethod
    def generate_token():
        return secrets.token_urlsafe()

    @staticmethod
    def encrypt_password(password: str):
        return hashlib.sha256(password.encode()).hexdigest()
