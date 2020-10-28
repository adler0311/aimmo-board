from flask_apispec import marshal_with

from backend.services.board_service import BoardLoadService
from backend.views.base_view import BaseView
from backend.schemas.board_schema import BoardSchema


class BoardsView(BaseView):

    @marshal_with(BoardSchema(many=True), code=200)
    def index(self):
        return BoardLoadService.get_many()
