from backend.schemas.comment import CommentSchema
from backend.models.comment import Comment
from backend.models.user import User
import pytest


@pytest.fixture
def comments():
    c = Comment(content="댓글입니다")
    c.pk = "5f85469378ebc3de6b8cf152"
    return [c]


def test_dump_comments_with_user():
    schema = CommentSchema()

    u = User()
    c = Comment(writer=u)

    result = schema.dump(c)

    assert result is not None
    assert result['writer'] is not None
    assert 'userId' in result['writer']


def test_load_comment_with_user():
    schema = CommentSchema()

    c = {'post_id': 'fff', 'content': '내용', 'writer': {
        'userId': '작성자'}}
    result = schema.load(c)

    assert result is not None
