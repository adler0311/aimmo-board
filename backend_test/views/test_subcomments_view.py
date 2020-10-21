from backend.models.subcomment import Subcomment
from unittest import mock
from pytest_flask.plugin import JSONResponse
from bson import ObjectId
from mongoengine import DoesNotExist
from typing import List
from backend.models.user import User
from backend.models.auth_token import AuthToken
import json
import pytest


from backend.models.post import Post
from backend.models.comment import Comment
from backend.schemas.comment_schema import CommentSchema


@mock.patch("backend.views.subcomments_view.Comment")
@mock.patch("backend.views.subcomments_view.Subcomment")
def test_get_subcomments(mock_subcomment, mock_comment, client):
    dummy_comment_id = 'aaaa'

    response: JSONResponse = client.get(
        '/comments/{}/subcomments/'.format(dummy_comment_id))

    assert response.status_code == 200


@pytest.fixture
def dummy_comment_id():
    return '5f85469378ebc3de6b8cf156'


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.schemas.subcomment_schema.SubcommentSchema.load")
@mock.patch("backend.views.subcomments_view.SubcommentService.add_subcomment")
def test_add_subcomment_is_authenticated(mock_add_subcomment, mock_load, mock_auth_token, client, dummy_comment_id):
    mock_add_subcomment.return_value = True
    valid_token = 'valid_token'

    headers = {'Content-Type': 'application/json',
               'Authorization': valid_token}

    data = {
        'content': '대댓글입니다',
    }

    mock_load.return_value = data

    response = client.post(
        '/comments/{}/subcomments/'.format(dummy_comment_id), data=json.dumps(data), headers=headers)

    assert response.status_code == 201


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.subcomments_view.Subcomment")
def test_put_comment_not_authorized(mock_subcomment, mock_auth_token, client):
    dummy_comment_id = '5f85469378ebc3de6b8cf156'
    dummy_subcomment_id = 'bf85469378ebc3de6b8cf156'

    writer = User(user_id='대댓글 작성자')
    writer.pk = 'uf85469378ebc3de6b8cf150'

    not_writer_token = 'not_writer_token'
    not_writer = User(user_id='사용자')
    not_writer.pk = 'uf85469378ebc3de6b8cf151'

    mock_subcomment.objects.get.return_value = Subcomment(writer=writer)
    mock_auth_token.objects.get.return_value = AuthToken(user=not_writer)
    data = {'content': '업데이트할 대댓글'}

    headers = {'Content-Type': 'application/json',
               'Authorization': not_writer_token}

    response = client.put(
        '/comments/{}/subcomments/{}'.format(dummy_comment_id,  dummy_subcomment_id), headers=headers, data=json.dumps(data))

    assert response.status_code == 403


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.subcomments_view.Subcomment")
@mock.patch("backend.views.subcomments_view.SubcommentSchema.load")
def test_put_comment_is_success(mock_load, mock_subcomment, mock_auth_token, client):
    dummy_comment_id = '5f85469378ebc3de6b8cf156'
    dummy_subcomment_id = 'bf85469378ebc3de6b8cf156'

    writer = User(user_id='대댓글 작성자')
    writer.pk = 'uf85469378ebc3de6b8cf150'
    writer_token = 'writer_token'
    data = {'content': '업데이트할 대댓글'}

    mock_subcomment.objects.get.return_value = Subcomment(writer=writer)
    mock_auth_token.objects.get.return_value = AuthToken(user=writer)
    mock_load.return_value = data

    headers = {'Content-Type': 'application/json',
               'Authorization': writer_token}

    response = client.put(
        '/comments/{comment_id}/subcomments/{subcomment_id}'.format(
            comment_id=dummy_comment_id, subcomment_id=dummy_subcomment_id),
        data=json.dumps(data), headers=headers)

    assert response.status_code == 200


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.subcomments_view.Subcomment")
def test_delete_comment_not_authorized(mock_subcomment, mock_auth_token, client):
    dummy_comment_id = '5f85469378ebc3de6b8cf156'
    dummy_subcomment_id = 'bf85469378ebc3de6b8cf156'

    writer = User(user_id='대댓글 작성자')
    writer.pk = 'uf85469378ebc3de6b8cf150'

    not_writer_token = 'writer_token'
    not_writer = User(user_id='사용자')
    not_writer.pk = 'uf85469378ebc3de6b8cf151'

    mock_subcomment.objects.get.return_value = Subcomment(writer=writer)
    mock_auth_token.objects.get.return_value = AuthToken(user=not_writer)

    headers = {'Content-Type': 'application/json',
               'Authorization': not_writer_token}

    response = client.delete(
        '/comments/{}/subcomments/{}/'.format(dummy_comment_id, dummy_subcomment_id), headers=headers)

    assert response.status_code == 403


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.subcomments_view.Subcomment")
@mock.patch("backend.views.subcomments_view.SubcommentService.delete_subcomment")
def test_delete_comment_is_success(mock_delete_subcomment, mock_subcomment, mock_auth_token, client):
    dummy_comment_id = '5f85469378ebc3de6b8cf156'
    dummy_subcomment_id = 'bf85469378ebc3de6b8cf156'
    mock_delete_subcomment.return_value = True

    writer = User(user_id='대댓글 작성자')
    writer.pk = 'uf85469378ebc3de6b8cf150'
    writer_token = 'writer_token'

    mock_subcomment.objects.get.return_value = Subcomment(writer=writer)
    mock_auth_token.objects.get.return_value = AuthToken(user=writer)

    headers = {'Content-Type': 'application/json',
               'Authorization': writer_token}

    response = client.delete(
        '/comments/{}/subcomments/{}/'.format(dummy_comment_id, dummy_subcomment_id), headers=headers)

    assert response.status_code == 200
