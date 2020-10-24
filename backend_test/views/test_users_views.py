from backend.models.auth_token import AuthToken
from backend_test.services.test_like_service import dummy_content_id
import json
from unittest import mock
from backend.models.user import User
from unittest import mock


def test_add_user_empty_data(client, default_header):

    response = client.post('/users/',  headers=default_header)

    assert response.status_code == 400


@mock.patch("backend.views.users_view.UserService.signup")
def test_add_user_success(mock_signup, client, default_header):
    mock_signup.return_value = 'dummy_token', User()
    data = {
        'userId': '아이디123',
        'password': '비밀번호123',
    }
    response = client.post(
        '/users/', data=json.dumps(data), headers=default_header)

    assert response.status_code == 201
    d = json.loads(response.data)
    assert d['token'] == 'dummy_token'


def test_get_contents_api_allowed(client):
    response = client.get('/users/contents/')
    assert response.status_code != 405


def test_get_contents_token_required(client, invalid_token_header):
    response = client.get('/users/contents/', headers=invalid_token_header)
    assert response.status_code == 401


@mock.patch("backend.views.decorators.AuthToken")
def test_get_contents_type_parameter_required(mock_auth_token, client, valid_token, valid_token_header):
    mock_auth_token.objects.get.return_value = AuthToken(token=valid_token)
    response = client.get('/users/contents/', headers=valid_token_header)

    assert response.status_code == 400
    d = json.loads(response.data)
    assert d['message'] == '"type" parameter required'


@mock.patch("backend.views.decorators.AuthToken")
def test_get_contents_type_parameter_invalid(mock_auth_token, client, valid_token, valid_token_header):
    mock_auth_token.objects.get.return_value = AuthToken(token=valid_token)
    response = client.get('/users/contents/?type=board',
                          headers=valid_token_header)

    assert response.status_code == 400
    d = json.loads(response.data)
    assert d['message'] == '"type" parameter shoud be one of ["post", "comment", "likePost"]'


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.users_view.UserService.get_user_contents")
@mock.patch("backend.views.users_view.PostSchema.dumps")
@mock.patch("backend.views.users_view.CommentSchema.dumps")
def test_get_contents_success(mock_comment_dumps, mock_post_dumps, mock_get_user_contents, mock_auth_token, client, valid_token, valid_token_header):
    mock_comment_dumps.return_value = []
    mock_post_dumps.return_value = []
    mock_get_user_contents.return_value = []
    mock_auth_token.objects.get.return_value = AuthToken(token=valid_token)

    response = client.get('/users/contents/?type=post',
                          headers=valid_token_header)

    assert response.status_code == 200
    d = json.loads(response.data)
    assert d['type'] == 'post'
    assert type(d['contents']) is list
