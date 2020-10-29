from mongoengine import DoesNotExist
from backend.models.auth_token import AuthToken
import json
from unittest import mock
from backend.models.user import User


def test_add_user_empty_data(client, default_header):
    response = client.post('/users',  headers=default_header)

    assert response.status_code == 422


@mock.patch("backend.views.users.UserSaveService.signup")
def test_add_user_success(mock_signup, client, default_header, valid_token):
    mock_signup.return_value = AuthToken(token=valid_token)
    data = {
        'userId': '아이디123',
        'password': '비밀번호123',
    }
    response = client.post('/users', data=json.dumps(data), headers=default_header)

    assert response.status_code == 201
    d = json.loads(response.data)
    assert d['token'] == valid_token


def test_get_contents_api_allowed(client):
    response = client.get('/users/posts')
    assert response.status_code != 405


@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
def test_get_posts_token_required(mock_get_auth_token, client, invalid_token_header):
    mock_get_auth_token.side_effect = DoesNotExist()

    response = client.get('/users/posts?type=like', headers=invalid_token_header)

    assert response.status_code == 401


@mock.patch("backend.views.decorators.AuthToken")
def test_get_contents_type_parameter_required(mock_auth_token, client, valid_token, valid_token_header):
    mock_auth_token.objects.get.return_value = AuthToken(token=valid_token)

    response = client.get('/users/posts', headers=valid_token_header)

    assert response.status_code == 422
    d = json.loads(response.data)
    assert d['message'] == '"type" parameter required'


@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
def test_get_contents_type_parameter_invalid(mock_get_auth_token, client, valid_token, valid_token_header):
    mock_get_auth_token.return_value = AuthToken(token=valid_token)

    response = client.get('/users/posts?type=write', headers=valid_token_header)

    assert response.status_code == 422


@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
@mock.patch("backend.views.users.UserLoadService.get_posts")
def test_get_posts_success(mock_get_posts, mock_get_auth_token, client, valid_token, valid_token_header):
    mock_get_posts.return_value = []
    mock_get_auth_token.return_value = AuthToken(token=valid_token, user=User(id=''))

    response = client.get('/users/posts?type=write', headers=valid_token_header)

    assert response.status_code == 200


@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
@mock.patch("backend.views.users.UserLoadService.get_liked_posts")
def test_get_liked_posts_success(mock_get_liked_posts, mock_get_auth_token, client, valid_token, valid_token_header):
    mock_get_liked_posts.return_value = []
    mock_get_auth_token.return_value = AuthToken(token=valid_token, user=User(id=''))

    response = client.get('/users/posts?type=like', headers=valid_token_header)

    assert response.status_code == 200


@mock.patch("backend.views.decorators.AuthTokenLoadService.get_auth_token")
@mock.patch("backend.views.users.UserLoadService.get_comments")
def test_get_comments_success(mock_get_comments, mock_get_auth_token, client, valid_token, valid_token_header):
    mock_get_comments.return_value = []
    mock_get_auth_token.return_value = AuthToken(token=valid_token, user=User(id=''))

    response = client.get('/users/comments', headers=valid_token_header)

    assert response.status_code == 200
