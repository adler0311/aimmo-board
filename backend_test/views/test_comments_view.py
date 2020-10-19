import json
import pytest
from unittest import mock
from pytest_flask.plugin import JSONResponse
from bson import ObjectId
from mongoengine import DoesNotExist
from typing import List
from backend.models.user import User
from backend.models.auth_token import AuthToken


from backend.models.post import Post
from backend.models.comment import Comment
from backend.schemas.comment_schema import CommentSchema


@pytest.fixture
def comments():
    u = User(user_id='user1')
    u.pk = 'uf85469378ebc3de6b8cf150'

    p = Post(title="게시글 제목", content="게시글 내용", writer=u)
    c1 = Comment(content='댓글입니다1', writer=u)
    c1.pk = '5f85469378ebc3de6b8cf154'
    c2 = Comment(content='댓글입니다2', writer=u)
    c2.pk = '5f85469378ebc3de6b8cf155'
    c3 = Comment(content='댓글입니다3', writer=u)
    c3.pk = '5f85469378ebc3de6b8cf156'

    return [c1, c2, c3]


@pytest.fixture
def writer():
    return {'userId': 'tester'}


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


@mock.patch("backend.views.decorators.AuthToken")
def test_add_comment_not_authenticated(mock_auth_token, client):
    dummy_post_id = '5f85469378ebc3de6b8cf156'
    invalid_token = 'invalid_token'

    mock_auth_token.objects.get.side_effect = DoesNotExist()

    headers = {'Content-Type': 'application/json',
               'Authorization': invalid_token}

    data = {'content': '내용'}

    response = client.post(
        '/posts/{}/comments/'.format(dummy_post_id), data=json.dumps(data), headers=headers)

    assert response.status_code == 401


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.schemas.comment_schema.CommentSchema")
@mock.patch("backend.views.comments_view.Post")
def test_add_comment_invalid_post(mock_post, mock_comment_schema, mock_auth_token, client):
    dummy_post_id = '5f85469378ebc3de6b8cf156'
    invalid_token = 'invalid_token'

    headers = {'Content-Type': 'application/json',
               'Authorization': invalid_token}

    data = {
        'content': '내용',
    }

    mock_post.objects.get.side_effect = DoesNotExist()
    mock_comment_schema().load.return_value = data

    response = client.post(
        '/posts/{}/comments/'.format(dummy_post_id), data=json.dumps(data), headers=headers)

    assert response.status_code == 404


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.schemas.comment_schema.CommentSchema")
@mock.patch("backend.views.comments_view.Post")
@mock.patch("backend.views.comments_view.Comment")
def test_add_comment_is_authenticated(mock_comment, mock_post, mock_comment_schema,
                                      mock_auth_token, client):

    dummy_post_id = '5f85469378ebc3de6b8cf156'
    valid_token = 'valid_token'

    headers = {'Content-Type': 'application/json',
               'Authorization': valid_token}

    data = {
        'content': '댓글입니다',
    }

    mock_comment_schema().load.return_value = data

    response = client.post(
        '/posts/{}/comments/'.format(dummy_post_id), data=json.dumps(data), headers=headers)

    assert response.status_code == 201


@mock.patch("backend.views.decorators.AuthToken")
def test_put_comment_not_authenticated(mock_auth_token, client, comments: List[Comment]):
    dummy_post_id = '5f85469378ebc3de6b8cf156'
    invalid_token = 'invalid_token'
    c = comments[0]

    mock_auth_token.objects.get.side_effect = DoesNotExist()

    headers = {'Content-Type': 'application/json',
               'Authorization': invalid_token}

    data = {'content': '내용'}

    response = client.put(
        '/posts/{post_id}/comments/{comment_id}'.format(
            post_id=dummy_post_id, comment_id=c.pk),
        data=json.dumps(data), headers=headers)

    assert response.status_code == 401


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.comments_view.Comment")
def test_put_comment_not_authorized(mock_comment, mock_auth_token, client, comments):
    dummy_post_id = '5f85469378ebc3de6b8cf156'
    c = comments[0]

    not_writer = User()
    not_writer.pk = 'nw85469378ebc3de6b8cf156'
    not_writer_token = 'not_writer_token'
    mock_auth_token.objects.get.return_value = AuthToken(user=not_writer)

    mock_comment.objects.get.return_value = c

    headers = {'Content-Type': 'application/json',
               'Authorization': not_writer_token}

    data = {'content': '업데이트할 댓글'}

    response = client.put(
        '/posts/{post_id}/comments/{comment_id}'.format(
            post_id=dummy_post_id, comment_id=c.pk),
        data=json.dumps(data), headers=headers)

    assert response.status_code == 403


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.comments_view.Comment")
def test_put_comment_is_success(mock_comment, mock_auth_token, client, comments):
    dummy_post_id = '5f85469378ebc3de6b8cf156'
    c = comments[0]

    writer = c.writer
    writer_token = 'writer_token'
    mock_auth_token.objects.get.return_value = AuthToken(user=writer)

    mock_comment.objects.get.return_value = c

    headers = {'Content-Type': 'application/json',
               'Authorization': writer_token}

    data = {'content': '업데이트할 댓글'}

    response = client.put(
        '/posts/{post_id}/comments/{comment_id}'.format(
            post_id=dummy_post_id, comment_id=c.pk),
        data=json.dumps(data), headers=headers)

    assert response.status_code == 200


@mock.patch("backend.views.decorators.AuthToken")
def test_delete_comment_not_authenticated(mock_auth_token, client, comments: List[Comment]):
    dummy_post_id = '5f85469378ebc3de6b8cf156'
    invalid_token = 'invalid_token'
    c = comments[0]

    mock_auth_token.objects.get.side_effect = DoesNotExist()

    headers = {'Content-Type': 'application/json',
               'Authorization': invalid_token}

    response = client.delete(
        '/posts/{post_id}/comments/{comment_id}/'.format(post_id=dummy_post_id, comment_id=c.pk), headers=headers)

    assert response.status_code == 401


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.comments_view.Comment")
def test_delete_comment_not_authorized(mock_comment, mock_auth_token, client, comments):
    dummy_post_id = '5f85469378ebc3de6b8cf156'
    c = comments[0]

    not_writer = User()
    not_writer.pk = 'nw85469378ebc3de6b8cf156'
    not_writer_token = 'not_writer_token'
    mock_auth_token.objects.get.return_value = AuthToken(user=not_writer)

    mock_comment.objects.get.return_value = c

    headers = {'Content-Type': 'application/json',
               'Authorization': not_writer_token}

    response = client.delete(
        '/posts/{post_id}/comments/{comment_id}/'.format(post_id=dummy_post_id, comment_id=c.pk), headers=headers)

    assert response.status_code == 403


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.comments_view.Comment")
@mock.patch("backend.views.comments_view.Post")
def test_delete_comment_is_success(mock_post, mock_comment, mock_auth_token, client, comments):
    dummy_post_id = '5f85469378ebc3de6b8cf156'
    c = comments[0]

    writer = c.writer
    writer_token = 'writer_token'
    mock_auth_token.objects.get.return_value = AuthToken(user=writer)

    mock_comment.objects.get.return_value = c

    headers = {'Content-Type': 'application/json',
               'Authorization': writer_token}

    response = client.delete(
        '/posts/{post_id}/comments/{comment_id}/'.format(post_id=dummy_post_id, comment_id=c.pk), headers=headers)

    assert response.status_code == 200
