from flask_apispec import marshal_with

from backend.services.board_service import BoardService
from backend.views.base_view import BaseView
from backend.schemas.board_schema import BoardSchema

service = BoardService()


class BoardsView(BaseView):

    @marshal_with(BoardSchema(many=True))
    def index(self):
        return service.get_many()
