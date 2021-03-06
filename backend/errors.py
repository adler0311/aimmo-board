class ForbiddenError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


class ApiError(Exception):
    def __init__(self, status_code, message=''):
        super().__init__()
        self.message = message
        self.status_code = status_code
