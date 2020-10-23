import json
from unittest import mock
from backend.models.user import User


def test_add_user_empty_data(client):
    headers = {'Content-Type': 'application/json'}

    response = client.post('/users/',  headers=headers)

    assert response.status_code == 400


@mock.patch("backend.views.users_view.UserService.signup")
def test_add_user_success(mock_signup, client):
    mock_signup.return_value = 'dummy_token', User()
    headers = {'Content-Type': 'application/json'}
    data = {
        'userId': '아이디123',
        'password': '비밀번호123',
    }
    response = client.post('/users/', data=json.dumps(data), headers=headers)

    assert response.status_code == 201
    d = json.loads(response.data)
    assert d['token'] == 'dummy_token'
