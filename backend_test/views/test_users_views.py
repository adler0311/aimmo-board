import pytest
import json
from unittest import mock
from pytest_flask.plugin import JSONResponse
from bson import ObjectId


@mock.patch("backend.views.users_view.User")
def test_add_user(mock_user, client):
    headers = {'Content-Type': 'application/json'}
    data = {
        'userId': '아이디123',
        'password': '비밀번호123',
    }

    response = client.post('/users/', data=json.dumps(data), headers=headers)

    assert response.status_code == 201
