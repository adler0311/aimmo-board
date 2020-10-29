import json
from unittest import mock
from backend.models.auth_token import AuthToken
from backend.models.user import User
import pytest


@pytest.fixture
def not_exist_user_id():
    return 'not_exist_user_id'


@mock.patch("backend.views.auth.AuthLoadService.sign_in")
def test_auth_user_not_exist(mock_sign_in, client, default_header, not_exist_user_id):
    mock_sign_in.return_value = None
    data = {
        'userId': not_exist_user_id,
        'password': 'dummy_password',
    }

    response = client.post(
        '/auth/', data=json.dumps(data), headers=default_header)

    assert response.status_code == 404


@mock.patch("backend.views.auth.AuthLoadService.sign_in")
def test_auth_success(mock_sign_in, client, default_header):
    u = User(user_id='test user')
    u.pk = 'pk123'
    mock_sign_in.return_value = AuthToken(token='token', user=u)

    data = {
        'userId': '아이디123',
        'password': '비밀번호123',
    }

    response = client.post(
        '/auth', data=json.dumps(data), headers=default_header)

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['user']['userId'] == 'test user'
    assert 'password' not in data['user']
    assert '_id' in data['user']
    assert data['user']['_id'] == 'pk123'


@mock.patch("backend.views.auth.AuthLoadService.sign_in")
def test_get(mock_sign_in, client, default_header):
    u = User(user_id='test user')
    u.pk = 'pk123'
    mock_sign_in.return_value = AuthToken(token='token', user=u)

    data = {
        'userId': '아이디123',
        'password': '비밀번호123',
    }

    response = client.post('/auth', data=json.dumps(data), headers=default_header)

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['user']['userId'] == 'test user'
    assert 'password' not in data['user']
    assert '_id' in data['user']
    assert data['user']['_id'] == 'pk123'
