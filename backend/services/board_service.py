from backend.models.board import Board


class BoardLoadService:
    @staticmethod
    def get_many(cls):
        return Board.objects()
