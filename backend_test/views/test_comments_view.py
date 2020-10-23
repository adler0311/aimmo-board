from backend_test.conftest import not_writer_token_header, writer_token_header
import json
import pytest
from unittest import mock
from pytest_flask.plugin import JSONResponse
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


@pytest.fixture
def dummy_post_id():
    return 'dummy_post_id'


@pytest.fixture
def dummy_post_id():
    return '5f85469378ebc3de6b8cf156'


@pytest.fixture
def dummy_data():
    return {'content': '내용'}


@mock.patch("backend.views.comments_view.Comment")
def test_get_comments(mock_post, client, comments, dummy_post_id):
    mock_post.objects.return_value = comments

    http_response: JSONResponse = client.get(
        '/posts/{}/comments/'.format(dummy_post_id))

    assert http_response.status_code == 200
    data = json.loads(http_response.data)
    assert data['postId'] == dummy_post_id

    schema = CommentSchema(many=True)
    result = schema.dump(comments)
    assert result == data['comments']


@mock.patch("backend.views.decorators.AuthToken")
def test_add_comment_not_authenticated(mock_auth_token, client, dummy_post_id, invalid_token_header):

    mock_auth_token.objects.get.side_effect = DoesNotExist()

    data = {'content': '내용'}

    response = client.post(
        '/posts/{}/comments/'.format(dummy_post_id), data=json.dumps(data),
        headers=invalid_token_header)

    assert response.status_code == 401


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.schemas.comment_schema.CommentSchema.load")
@mock.patch("backend.views.comments_view.CommentService.post")
def test_add_comment_invalid_post(mock_post, mock_load, mock_auth_token,
                                  client, dummy_post_id, invalid_token_header, dummy_data):

    mock_post.return_value = False
    mock_load.return_value = dummy_data

    response = client.post(
        '/posts/{}/comments/'.format(dummy_post_id), data=json.dumps(dummy_data),
        headers=invalid_token_header)

    assert response.status_code == 404


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.schemas.comment_schema.CommentSchema.load")
@mock.patch("backend.views.comments_view.CommentService.post")
def test_add_comment_is_authenticated(mock_post, mock_load, mock_auth_token, client,
                                      dummy_post_id, valid_token_header, dummy_data):

    mock_post.return_value = True
    mock_load.return_value = dummy_data

    response = client.post(
        '/posts/{}/comments/'.format(dummy_post_id), data=json.dumps(dummy_data),
        headers=valid_token_header)

    assert response.status_code == 201


@mock.patch("backend.views.decorators.AuthToken")
def test_put_comment_not_authenticated(mock_auth_token, client,
                                       comments: List[Comment], dummy_post_id, invalid_token_header, dummy_data):
    c = comments[0]

    mock_auth_token.objects.get.side_effect = DoesNotExist()

    response = client.put(
        '/posts/{post_id}/comments/{comment_id}'.format(
            post_id=dummy_post_id, comment_id=c.pk),
        data=json.dumps(dummy_data), headers=invalid_token_header)

    assert response.status_code == 401


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.comments_view.Comment")
def test_put_comment_not_authorized(mock_comment, mock_auth_token, client,
                                    comments, dummy_post_id, not_writer_token_header):
    c = comments[0]

    not_writer = User()
    not_writer.pk = 'nw85469378ebc3de6b8cf156'

    mock_auth_token.objects.get.return_value = AuthToken(user=not_writer)

    mock_comment.objects.get.return_value = c

    data = {'content': '업데이트할 댓글'}

    response = client.put(
        '/posts/{post_id}/comments/{comment_id}'.format(
            post_id=dummy_post_id, comment_id=c.pk),
        data=json.dumps(data), headers=not_writer_token_header)

    assert response.status_code == 403


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.comments_view.Comment")
@mock.patch("backend.views.comments_view.CommentSchema.load")
def test_put_comment_is_success(mock_load, mock_comment, mock_auth_token, client,
                                comments, dummy_post_id, writer_token_header):
    c = comments[0]

    writer = c.writer

    data = {'content': '업데이트할 댓글'}

    mock_auth_token.objects.get.return_value = AuthToken(user=writer)
    mock_comment.objects.get.return_value = c
    mock_load.retun_value = data

    response = client.put(
        '/posts/{post_id}/comments/{comment_id}'.format(
            post_id=dummy_post_id, comment_id=c.pk),
        data=json.dumps(data), headers=writer_token_header)

    assert response.status_code == 200


@mock.patch("backend.views.decorators.AuthToken")
def test_delete_comment_not_authenticated(mock_auth_token, client,
                                          comments: List[Comment], dummy_post_id, invalid_token_header):
    c = comments[0]

    mock_auth_token.objects.get.side_effect = DoesNotExist()

    response = client.delete(
        '/posts/{post_id}/comments/{comment_id}/'.format(
            post_id=dummy_post_id, comment_id=c.pk),
        headers=invalid_token_header)

    assert response.status_code == 401


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.comments_view.Comment")
def test_delete_comment_not_authorized(mock_comment, mock_auth_token, client,
                                       comments, dummy_post_id, not_writer_token_header):
    c = comments[0]

    not_writer = User()
    not_writer.pk = 'nw85469378ebc3de6b8cf156'
    mock_auth_token.objects.get.return_value = AuthToken(user=not_writer)

    mock_comment.objects.get.return_value = c

    response = client.delete(
        '/posts/{post_id}/comments/{comment_id}/'.format(
            post_id=dummy_post_id, comment_id=c.pk),
        headers=not_writer_token_header)

    assert response.status_code == 403


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.comments_view.Comment")
@mock.patch("backend.views.comments_view.CommentService.delete")
def test_delete_comment_is_success(mock_delete, mock_comment, mock_auth_token, client,
                                   comments: List[Comment], dummy_post_id, writer_token_header):
    c = comments[0]

    writer = c.writer
    mock_auth_token.objects.get.return_value = AuthToken(user=writer)

    mock_comment.objects.get.return_value = c
    mock_delete.return_value = True

    response = client.delete(
        '/posts/{post_id}/comments/{comment_id}/'.format(
            post_id=dummy_post_id, comment_id=c.pk),
        headers=writer_token_header)

    assert response.status_code == 200
