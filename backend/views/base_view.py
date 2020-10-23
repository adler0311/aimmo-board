from backend.views.decorators import handle_internal_server_error
from flask_classful import FlaskView

class BaseView(FlaskView):
    decorators = [handle_internal_server_error]
