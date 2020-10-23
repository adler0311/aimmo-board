from backend.views.base_view import BaseView
from backend.models.board import Board
from backend.schemas.board_schema import BoardSchema

boards_response = BoardSchema(many=True)


class BoardsView(BaseView):

    def index(self):
        boards = Board.objects()
        result = boards_response.dump(boards)
        return {'boards': result}
