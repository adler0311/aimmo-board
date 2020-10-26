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

    response: JSONResponse = client.get(
        '/comments/{}/subcomments/'.format(dummy_comment_id))

    assert response.status_code == 200


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.schemas.subcomment_schema.SubcommentSchema.load")
@mock.patch("backend.views.subcomments_view.SubcommentService.post")
def test_add_subcomment_is_authenticated(mock_post, mock_load, mock_auth_token, client,
                                         dummy_comment_id, valid_token_header):
    mock_post.return_value = True

    data = {
        'content': '대댓글입니다',
    }

    mock_load.return_value = data

    response = client.post(
        '/comments/{}/subcomments/'.format(dummy_comment_id), data=json.dumps(data), headers=valid_token_header)

    assert response.status_code == 201


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.subcomments_view.Subcomment")
def test_put_subcomment_not_authorized(mock_subcomment, mock_auth_token, client,
                                       not_writer_token_header, dummy_comment_id, dummy_subcomment_id):
    writer = User(user_id='대댓글 작성자')
    writer.pk = 'uf85469378ebc3de6b8cf150'

    not_writer = User(user_id='사용자')
    not_writer.pk = 'uf85469378ebc3de6b8cf151'

    data = {'content': '업데이트할 대댓글'}

    mock_subcomment.objects.get.return_value = Subcomment(writer=writer)
    mock_auth_token.objects.get.return_value = AuthToken(user=not_writer)

    response = client.put(
        '/comments/{}/subcomments/{}'.format(dummy_comment_id,  dummy_subcomment_id), headers=not_writer_token_header, data=json.dumps(data))

    assert response.status_code == 403


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.subcomments_view.Subcomment")
@mock.patch("backend.views.subcomments_view.SubcommentSchema.load")
@mock.patch("backend.views.subcomments_view.SubcommentService.update")
def test_put_subcomment_is_success(mock_update, mock_load, mock_subcomment, mock_auth_token, client,
                                   writer_token_header, dummy_comment_id, dummy_subcomment_id):

    writer = User(user_id='대댓글 작성자')
    writer.pk = 'uf85469378ebc3de6b8cf150'

    data = {'content': '업데이트할 대댓글'}

    mock_update.return_value = 1
    mock_subcomment.objects.get.return_value = Subcomment(writer=writer)
    mock_auth_token.objects.get.return_value = AuthToken(user=writer)
    mock_load.return_value = data

    response = client.put(
        '/comments/{comment_id}/subcomments/{subcomment_id}'.format(
            comment_id=dummy_comment_id, subcomment_id=dummy_subcomment_id),
        data=json.dumps(data), headers=writer_token_header)

    assert response.status_code == 200


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.subcomments_view.Subcomment")
def test_delete_subcomment_not_authorized(mock_subcomment, mock_auth_token, client,
                                          not_writer_token_header, dummy_comment_id, dummy_subcomment_id):

    writer = User(user_id='대댓글 작성자')
    writer.pk = 'uf85469378ebc3de6b8cf150'

    not_writer = User(user_id='사용자')
    not_writer.pk = 'uf85469378ebc3de6b8cf151'

    mock_subcomment.objects.get.return_value = Subcomment(writer=writer)
    mock_auth_token.objects.get.return_value = AuthToken(user=not_writer)

    response = client.delete(
        '/comments/{}/subcomments/{}/'.format(dummy_comment_id, dummy_subcomment_id), headers=not_writer_token_header)

    assert response.status_code == 403


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.subcomments_view.Subcomment")
@mock.patch("backend.views.subcomments_view.SubcommentService.delete")
def test_delete_subcomment_is_success(mock_delete, mock_subcomment, mock_auth_token, client,
                                      writer_token_header, dummy_comment_id, dummy_subcomment_id):
    mock_delete.return_value = True

    writer = User(user_id='대댓글 작성자')
    writer.pk = 'uf85469378ebc3de6b8cf150'

    mock_subcomment.objects.get.return_value = Subcomment(writer=writer)
    mock_auth_token.objects.get.return_value = AuthToken(user=writer)

    response = client.delete(
        '/comments/{}/subcomments/{}/'.format(
            dummy_comment_id, dummy_subcomment_id),
        headers=writer_token_header)

    assert response.status_code == 200
