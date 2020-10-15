import json
import pytest
from unittest import mock
from pytest_flask.plugin import JSONResponse
from bson import ObjectId
from mongoengine import DoesNotExist


from backend.models.post import Post
from backend.models.comment import Comment
from backend.schemas.comment_schema import CommentSchema


@pytest.fixture
def comments():
    p = Post(title="게시글 제목", content="게시글 내용", writer="게시글 작성자")
    c1 = Comment(content='댓글입니다1', writer='writer1')
    c1.pk = '5f85469378ebc3de6b8cf154'
    c2 = Comment(content='댓글입니다2', writer='writer2')
    c2.pk = '5f85469378ebc3de6b8cf155'
    c3 = Comment(content='댓글입니다3', writer='writer3')
    c3.pk = '5f85469378ebc3de6b8cf156'

    return [c1, c2, c3]


@mock.patch("backend.views.comments_view.Comment")
def test_get_comments(mock_post, client, comments):
    mock_post.objects.return_value = comments
    dummy_post_id = 'aaaa'

    http_response: JSONResponse = client.get(
        '/posts/{}/comments/'.format(dummy_post_id))

    assert http_response.status_code == 200
    data = json.loads(http_response.data)
    assert data['postId'] == dummy_post_id

    schema = CommentSchema(many=True)
    result = schema.dump(comments)
    assert result == data['comments']
