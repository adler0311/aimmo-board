import json
import pytest
from unittest import mock
from pytest_flask.plugin import JSONResponse
from bson import ObjectId
from mongoengine import DoesNotExist
from typing import List


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


@mock.patch("backend.views.comments_view.Comment")
@mock.patch("backend.views.comments_view.Post")
@mock.patch("backend.views.comments_view.CommentSchema")
def test_add_comment(mock_comment_schema, mock_post, mock_comment, client):

    dummy_post_id = '5f85469378ebc3de6b8cf156'
    headers = {'Content-Type': 'application/json'}
    data = {
        'content': '내용',
        'writer': '작성자',
        'post_id': dummy_post_id
    }

    mock_comment_schema().load.return_value = data

    response = client.post(
        '/posts/{}/comments/'.format(dummy_post_id), data=json.dumps(data), headers=headers)

    assert response.status_code == 201


@mock.patch("backend.views.comments_view.Comment")
def test_put_comment(mock_comment, client, comments: List[Comment]):
    mock_comment.objects.update_one.return_value = 1
    dummy_post_id = '5f85469378ebc3de6b8cf156'

    c = comments[0]

    headers = {'Content-Type': 'application/json'}
    data = {
        'content': '내용',
        'writer': '작성자',
    }

    response = client.put(
        '/posts/{post_id}/comments/{comment_id}'.format(
            post_id=dummy_post_id, comment_id=c.pk),
        data=json.dumps(data), headers=headers)

    assert response.status_code == 200


@mock.patch("backend.views.comments_view.Comment")
@mock.patch("backend.views.comments_view.Post")
def test_delete_comment(mock_post, mock_comment, client, comments: List[Comment]):
    dummy_post_id = '5f85469378ebc3de6b8cf156'
    c = comments[0]
    response = client.delete(
        '/posts/{post_id}/comments/{comment_id}'.format(post_id=dummy_post_id, comment_id=c.pk))

    assert response.status_code == 200


# @mock.patch("backend.views.comments_view.CommentSchema")
# @mock.patch("backend.views.comments_view.Comment")
# def test_add_comment_with_bad_request(mock_comment, mock_comment_schema, client):
#     vr = ValueError()
#     vr.messages = 'bad request error'
#     mock_comment_schema().load.side_effect = vr

#     dummy_post_id = '5f85469378ebc3de6b8cf156'
#     headers = {'Content-Type': 'application/json'}
#     data = {
#         'content': '내용',
#         'writer': '작성자',
#         'post_id': dummy_post_id
#     }

#     response = client.post(
#         '/posts/{}/comments/'.format(dummy_post_id), data=json.dumps(data), headers=headers)

#     assert response.status_code == 400
