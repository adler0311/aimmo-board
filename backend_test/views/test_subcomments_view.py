from backend_test.conftest import not_writer_token_header, valid_token_header, writer_token_header
from backend.models.subcomment import Subcomment
from unittest import mock
from pytest_flask.plugin import JSONResponse
from backend.models.user import User
from backend.models.auth_token import AuthToken
import json
import pytest


@pytest.fixture
def dummy_comment_id():
    return '5f85469378ebc3de6b8cf156'


@pytest.fixture
def dummy_subcomment_id():
    return 'bf85469378ebc3de6b8cf156'


@mock.patch("backend.views.subcomments_view.SubcommentService.get_many")
def test_get_subcomments(mock_get_many, client, dummy_comment_id):
    mock_get_many.return_value = []

    response: JSONResponse = client.get('/comments/{}/sub-comments/'.format(dummy_comment_id))

    assert response.status_code == 200


@mock.patch("backend.views.decorators.AuthService.get_auth_token")
@mock.patch("backend.views.subcomments_view.SubcommentService.post")
def test_add_subcomment_is_success(mock_post_method, mock_get_auth_token, client, dummy_comment_id, valid_token_header):
    mock_get_auth_token.return_value = True
    mock_post_method.return_value = True

    data = {
        'content': '대댓글입니다',
    }

    response = client.post(
        '/comments/{}/sub-comments/'.format(dummy_comment_id), data=json.dumps(data), headers=valid_token_header)

    assert response.status_code == 201


@mock.patch("backend.views.decorators.AuthService.get_auth_token")
@mock.patch("backend.views.subcomments_view.SubcommentService.is_writer")
def test_put_sub_comment_not_authorized(mock_is_writer, mock_get_auth_token, client,
                                       not_writer_token_header, dummy_comment_id, dummy_subcomment_id):
    not_writer = User(user_id='사용자')
    data = {'content': '업데이트할 대댓글'}

    mock_is_writer.return_value = False
    mock_get_auth_token.return_value = AuthToken(user=not_writer)

    response = client.put(
        '/comments/{}/sub-comments/{}'.format(dummy_comment_id,  dummy_subcomment_id), headers=not_writer_token_header, data=json.dumps(data))

    assert response.status_code == 403


@mock.patch("backend.views.decorators.AuthService.get_auth_token")
@mock.patch("backend.views.subcomments_view.SubcommentService.is_writer")
@mock.patch("backend.views.subcomments_view.SubcommentService.update")
def test_put_sub_comment_is_success(mock_update, mock_is_writer, mock_auth_token, client, writer_token_header,
                                    dummy_comment_id, dummy_subcomment_id):

    writer = User(user_id='대댓글 작성자')
    data = {'content': '업데이트할 대댓글'}

    mock_auth_token.return_value = AuthToken(user=writer)
    mock_is_writer.return_value = True
    mock_update.return_value = 1

    response = client.put('/comments/{comment_id}/sub-comments/{subcomment_id}'.format(
            comment_id=dummy_comment_id, subcomment_id=dummy_subcomment_id), data=json.dumps(data), headers=writer_token_header)

    assert response.status_code == 200


@mock.patch("backend.views.decorators.AuthService.get_auth_token")
@mock.patch("backend.views.subcomments_view.SubcommentService.is_writer")
def test_delete_subcomment_not_authorized(mock_is_writer, mock_get_auth_token, client,
                                          not_writer_token_header, dummy_comment_id, dummy_subcomment_id):
    not_writer = User(user_id='사용자')

    mock_get_auth_token.return_value = AuthToken(user=not_writer)
    mock_is_writer.return_value = False

    response = client.delete(
        '/comments/{}/sub-comments/{}'.format(dummy_comment_id, dummy_subcomment_id), headers=not_writer_token_header)

    assert response.status_code == 403


@mock.patch("backend.views.decorators.AuthService.get_auth_token")
@mock.patch("backend.views.subcomments_view.SubcommentService.is_writer")
@mock.patch("backend.views.subcomments_view.SubcommentService.delete")
def test_delete_subcomment_is_success(mock_delete, mock_is_writer, mock_get_auth_token, client,
                                      writer_token_header, dummy_comment_id, dummy_subcomment_id):

    writer = User(user_id='대댓글 작성자')

    mock_get_auth_token.return_value = AuthToken(user=writer)
    mock_is_writer.return_value = True
    mock_delete.return_value = True

    response = client.delete(
        '/comments/{}/sub-comments/{}'.format(dummy_comment_id, dummy_subcomment_id), headers=writer_token_header)

    assert response.status_code == 200
