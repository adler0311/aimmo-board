import secrets
import hashlib


class Utils:
    @staticmethod
    def generate_token():
        return secrets.token_urlsafe()

    @staticmethod
    def encrypt_password(password: str):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def page_limit_to_start_end(page, limit):
        return (page - 1) * limit, page * limit
