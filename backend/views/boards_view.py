from flask_classful import FlaskView
from backend.models.board import Board
from backend.schemas.board_schema import BoardSchema
from mongoengine import DoesNotExist, QuerySet
from backend.views.decorators import token_required, input_data_required
from marshmallow import ValidationError
import logging
from backend.views.decorators import handle_internal_server_error

boards_response = BoardSchema(many=True)


class BoardsView(FlaskView):
    decorators = [handle_internal_server_error]

    def index(self):
        boards = Board.objects()
        result = boards_response.dump(boards)
        return {'boards': result}
