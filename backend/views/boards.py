from flask_apispec import marshal_with

from backend.models.board import Board
from backend.views.base import BaseView
from backend.schemas.board import BoardSchema


class BoardsView(BaseView):

    @marshal_with(BoardSchema(many=True), code=200)
    def index(self):
        return Board.objects()
