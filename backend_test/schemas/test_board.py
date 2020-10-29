from backend.models.board import Board
from backend.schemas.board import BoardSchema


def test_dump():
    schema = BoardSchema()
    b = Board(title="자유게시판")
    b.pk = "gf85469378ebc3de6b8cf152"

    result = schema.dump(b)

    assert result is not None
    assert result['_id'] is "gf85469378ebc3de6b8cf152"
