import secrets


class Utils:
    @staticmethod
    def generate_token():
        return secrets.token_urlsafe()
