import pytest
import json
from unittest import mock
from pytest_flask.plugin import JSONResponse
from bson import ObjectId
from backend.models.user import User


@mock.patch("backend.views.auth_view.AuthToken")
@mock.patch("backend.views.auth_view.User")
def test_auth(mock_user, mock_auth_token, client):
    objects = mock_user.objects()
    u = User(user_id='test user')
    u.pk = 'pk123'
    objects.first.return_value = u

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
