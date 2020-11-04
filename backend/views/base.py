from backend.views.decorators import handle_forbidden_error, handle_internal_server_error, handle_not_found_error
from flask_classful import FlaskView


class BaseView(FlaskView):
    decorators = [handle_internal_server_error, handle_not_found_error, handle_forbidden_error]
