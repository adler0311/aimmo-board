from unittest import mock
from pytest_flask.plugin import JSONResponse
from backend.models.user import User
from backend.models.auth_token import AuthToken
import json
import pytest


@pytest.fixture
def dummy_board_id():
    return 'dummy_board_id'


@pytest.fixture
def dummy_post_id():
    return 'dummy_post_id'


@pytest.fixture
def dummy_comment_id():
    return '5f85469378ebc3de6b8cf156'


@pytest.fixture
def dummy_sub_comment_id():
    return 'bf85469378ebc3de6b8cf156'


@mock.patch("backend.views.subcomments.SubCommentLoadService.get_many")
def test_get_sub_comments(mock_get_many, client, dummy_comment_id, dummy_board_id, dummy_post_id):
    mock_get_many.return_value = []

    response: JSONResponse = client.get('/boards/{}/posts/{}/comments/{}/sub-comments'.format(dummy_board_id, dummy_post_id, dummy_comment_id))

    assert response.status_code == 200


@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
@mock.patch("backend.views.subcomments.SubCommentSaveService.post")
def test_add_sub_comment_is_success(mock_post_method, mock_get_auth_token, client, dummy_comment_id, valid_token_header, dummy_board_id, dummy_post_id):
    mock_get_auth_token.return_value = AuthToken()
    mock_post_method.return_value = True
    data = {'content': '대댓글입니다'}

    response = client.post('/boards/{}/posts/{}/comments/{}/sub-comments'.format(dummy_board_id, dummy_post_id, dummy_comment_id),
                           data=json.dumps(data), headers=valid_token_header)

    assert response.status_code == 201


@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
@mock.patch("backend.views.subcomments.SubCommentCheckService.is_writer")
def test_put_sub_comment_not_authorized(mock_is_writer, mock_get_auth_token, client, not_writer_token_header, dummy_comment_id,
                                        dummy_sub_comment_id, dummy_board_id, dummy_post_id):
    not_writer = User(user_id='사용자')
    data = {'content': '업데이트할 대댓글'}

    mock_is_writer.return_value = False
    mock_get_auth_token.return_value = AuthToken(user=not_writer)

    response = client.put('/boards/{}/posts/{}/comments/{}/sub-comments/{}'.format(dummy_board_id, dummy_post_id, dummy_comment_id,  dummy_sub_comment_id),
                          headers=not_writer_token_header, data=json.dumps(data))

    assert response.status_code == 403


@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
@mock.patch("backend.views.subcomments.SubCommentCheckService.is_writer")
@mock.patch("backend.views.subcomments.SubCommentModifyService.update")
def test_put_sub_comment_is_success(mock_update, mock_is_writer, mock_auth_token, client, writer_token_header,
                                    dummy_comment_id, dummy_sub_comment_id, dummy_board_id, dummy_post_id):

    writer = User(user_id='대댓글 작성자')
    data = {'content': '업데이트할 대댓글'}

    mock_auth_token.return_value = AuthToken(user=writer)
    mock_is_writer.return_value = True
    mock_update.return_value = 1

    response = client.put('/boards/{}/posts/{}/comments/{}/sub-comments/{}'.format(
        dummy_board_id, dummy_post_id, dummy_comment_id, dummy_sub_comment_id), data=json.dumps(data), headers=writer_token_header)

    assert response.status_code == 200


@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
@mock.patch("backend.views.subcomments.SubCommentCheckService.is_writer")
def test_delete_sub_comment_not_authorized(mock_is_writer, mock_get_auth_token, client, not_writer_token_header, dummy_comment_id,
                                          dummy_sub_comment_id, dummy_board_id, dummy_post_id):
    not_writer = User(user_id='사용자')

    mock_get_auth_token.return_value = AuthToken(user=not_writer)
    mock_is_writer.return_value = False

    response = client.delete('/boards/{}/posts/{}/comments/{}/sub-comments/{}'.format(
        dummy_board_id, dummy_post_id, dummy_comment_id, dummy_sub_comment_id), headers=not_writer_token_header)

    assert response.status_code == 403


@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
@mock.patch("backend.views.subcomments.SubCommentCheckService.is_writer")
@mock.patch("backend.views.subcomments.SubCommentRemoveService.delete")
def test_delete_sub_comment_is_success(mock_delete, mock_is_writer, mock_get_auth_token, client, writer_token_header, dummy_comment_id,
                                       dummy_sub_comment_id, dummy_board_id, dummy_post_id):

    writer = User(user_id='대댓글 작성자')

    mock_get_auth_token.return_value = AuthToken(user=writer)
    mock_is_writer.return_value = True
    mock_delete.return_value = True

    response = client.delete('/boards/{}/posts/{}/comments/{}/sub-comments/{}'.format(
        dummy_board_id, dummy_post_id, dummy_comment_id, dummy_sub_comment_id), headers=writer_token_header)

    assert response.status_code == 200
