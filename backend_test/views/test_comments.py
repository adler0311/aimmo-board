import json
import pytest
from unittest import mock
from pytest_flask.plugin import JSONResponse
from mongoengine import DoesNotExist
from typing import List
from backend.models.user import User
from backend.models.auth_token import AuthToken

from backend.models.comment import Comment
from backend.schemas.comment import CommentSchema


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
def dummy_board_id():
    return 'dummy_board_id'


@pytest.fixture
def dummy_data():
    return {'content': '내용'}

@pytest.fixture
def dummy_comment_id():
    return 'dummy_comment_id'


@mock.patch("backend.views.comments.Comment")
def test_get_comments(mock_post, client, comments, dummy_post_id):
    mock_post.objects.return_value = comments

    http_response: JSONResponse = client.get(
        '/posts/{}/comments/'.format(dummy_post_id))

    assert http_response.status_code == 200
    data = json.loads(http_response.data)

    schema = CommentSchema(many=True)
    result = schema.dump(comments)
    assert result == data


@mock.patch("backend.views.comments.CommentLoadService.get_one")
def test_get_comment_is_success(mock_get_one, client,dummy_board_id, dummy_post_id, dummy_comment_id, comments):
    mock_get_one.return_value = comments[0], True
    response = client.get('boards/{}/posts/{}/comments/{}'.format(dummy_board_id, dummy_post_id, dummy_comment_id))

    assert response.status_code == 200
    data = json.loads(response.data)
    schema = CommentSchema()
    result = schema.dump((comments[0]))
    assert result == data


@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
def test_add_comment_not_authenticated(mock_get_auth_token, client, dummy_post_id, invalid_token_header, dummy_board_id):
    mock_get_auth_token.side_effect = DoesNotExist()
    data = {'content': '내용'}

    response = client.post('boards/{}/posts/{}/comments'.format(dummy_board_id, dummy_post_id), data=json.dumps(data), headers=invalid_token_header)

    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['message'] == 'not authenticated'


@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
@mock.patch("backend.views.comments.CommentSaveService.post")
def test_add_comment_invalid_post(mock_post, mock_get_auth_token, client, dummy_post_id, invalid_token_header, dummy_data):

    mock_post.return_value = False
    mock_get_auth_token.return_value = AuthToken()

    response = client.post('boards/{}/posts/{}/comments'.format(dummy_board_id, dummy_post_id), data=json.dumps(dummy_data), headers=invalid_token_header)

    assert response.status_code == 404


@mock.patch("backend.views.comments.CommentSaveService.post")
def test_add_comment_is_authenticated(mock_post, client, dummy_post_id, valid_token_header, dummy_data):

    mock_post.return_value = True

    response = client.post(
        '/posts/{}/comments/'.format(dummy_post_id), data=json.dumps(dummy_data),
        headers=valid_token_header)

    assert response.status_code == 201


@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
def test_put_comment_not_authenticated(mock_get_auth_token, client, comments: List[Comment], dummy_post_id, invalid_token_header, dummy_data, dummy_board_id):
    c = comments[0]

    mock_get_auth_token.side_effect = DoesNotExist()

    response = client.put('boards/{}/posts/{}/comments/{}'.format(dummy_board_id, dummy_post_id, c.pk), data=json.dumps(dummy_data),
                          headers=invalid_token_header)

    assert response.status_code == 401


@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
@mock.patch("backend.views.comments.CommentCheckService.is_writer")
def test_put_comment_not_authorized(mock_is_writer,  mock_get_auth_token, client, comments, dummy_post_id, not_writer_token_header, dummy_board_id):
    c = comments[0]
    not_writer = User()
    not_writer.pk = 'nw85469378ebc3de6b8cf156'
    data = {'content': '업데이트할 댓글'}

    mock_get_auth_token.return_value = AuthToken(user=not_writer)
    mock_is_writer.return_value = False

    response = client.put('/boards/{board_id}/posts/{post_id}/comments/{comment_id}'.format(board_id=dummy_board_id, post_id=dummy_post_id, comment_id=c.pk),
                          data=json.dumps(data), headers=not_writer_token_header)

    assert response.status_code == 403


@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
@mock.patch("backend.views.comments.CommentModifyService.update")
@mock.patch("backend.views.comments.CommentCheckService.is_writer")
def test_put_comment_is_success(mock_is_writer, mock_update, mock_get_auth_token, client, comments, dummy_post_id, writer_token_header, dummy_board_id):
    c = comments[0]

    writer = c.writer

    data = {'content': '업데이트할 댓글'}
    mock_get_auth_token.return_value = AuthToken(user=writer)
    mock_is_writer.return_value = True
    mock_update.return_value = c

    response = client.put('/boards/{board_id}/posts/{post_id}/comments/{comment_id}'.format(board_id=dummy_board_id, post_id=dummy_post_id, comment_id=c.pk),
                          data=json.dumps(data), headers=writer_token_header)

    assert response.status_code == 200


@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
def test_delete_comment_not_authenticated(mock_get_auth_token, client,
                                          comments: List[Comment], dummy_post_id, invalid_token_header):
    c = comments[0]
    mock_get_auth_token.side_effect = DoesNotExist()

    response = client.delete('/boards/{board_id}/posts/{post_id}/comments/{comment_id}'.format(board_id=dummy_board_id, post_id=dummy_post_id, comment_id=c.pk),
                             headers=invalid_token_header)

    assert response.status_code == 401


@mock.patch("backend.views.comments.CommentCheckService.is_writer")
@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
def test_delete_comment_not_authorized(mock_get_auth_token, mock_is_writer, client, comments, dummy_post_id, not_writer_token_header, dummy_board_id):
    c = comments[0]
    not_writer = User()
    not_writer.pk = 'nw85469378ebc3de6b8cf156'

    mock_get_auth_token.return_value = AuthToken(user=not_writer)
    mock_is_writer.return_value = False

    response = client.delete('/boards/{board_id}/posts/{post_id}/comments/{comment_id}'.format(board_id=dummy_board_id, post_id=dummy_post_id, comment_id=c.pk),
                             headers=not_writer_token_header)

    assert response.status_code == 403


@mock.patch("backend.views.comments.CommentCheckService.is_writer")
@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
@mock.patch("backend.views.comments.CommentRemoveService.delete")
def test_delete_comment_is_success(mock_delete, mock_get_auth_token, mock_is_writer, client,
                                   comments: List[Comment], dummy_post_id, writer_token_header,dummy_board_id):
    c = comments[0]

    mock_get_auth_token.return_value = AuthToken(user=c.writer)
    mock_is_writer.return_value = True
    mock_delete.return_value = True

    response = client.delete('/boards/{board_id}/posts/{post_id}/comments/{comment_id}'.format(board_id=dummy_board_id, post_id=dummy_post_id, comment_id=c.pk),
                             headers=writer_token_header)

    assert response.status_code == 200
