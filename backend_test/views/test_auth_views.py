import json
from unittest import mock
from backend.models.user import User


@mock.patch("backend.views.auth_view.AuthService.sign_in")
def test_auth_user_not_exist(mock_sign_in, client):
    mock_sign_in.return_value = None, None

    headers = {'Content-Type': 'application/json'}
    data = {
        'userId': 'user_not_exist_id',
        'password': 'dummy_password',
    }

    response = client.post('/auth/', data=json.dumps(data), headers=headers)

    assert response.status_code == 404


@mock.patch("backend.views.auth_view.AuthService.sign_in")
def test_auth_success(mock_sign_in, client):
    u = User(user_id='test user')
    u.pk = 'pk123'
    mock_sign_in.return_value = 'dummy_token', u

    headers = {'Content-Type': 'application/json'}
    data = {
        'userId': '아이디123',
        'password': '비밀번호123',
    }

    response = client.post('/auth/', data=json.dumps(data), headers=headers)

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['user']['userId'] == 'test user'
    assert 'password' not in data['user']
    assert '_id' in data['user']
    assert data['user']['_id'] == 'pk123'
