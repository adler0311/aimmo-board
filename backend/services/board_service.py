from backend.models.board import Board


class BoardService:
    def get_many(self):
        return Board.objects()
