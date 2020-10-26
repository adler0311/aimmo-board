from backend.services.board_service import BoardService
from backend.views.base_view import BaseView
from backend.schemas.board_schema import BoardSchema

boards_response = BoardSchema(many=True)
service = BoardService()


class BoardsView(BaseView):

    def index(self):
        boards = service.get_many()
        result = boards_response.dump(boards)
        return {'boards': result}
