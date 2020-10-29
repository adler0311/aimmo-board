from backend.models.board import Board


class BoardLoadService:
    @classmethod
    def get_many(cls):
        return Board.objects()
