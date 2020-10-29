import pytest
import json
from unittest import mock
from pytest_flask.plugin import JSONResponse
from backend.models.board import Board


@pytest.fixture
def boards():
    b1 = Board(title='자유게시판')
    b1.pk = '5f85469378ebc3de6b8cf154'
    b2 = Board(title='부동산')
    b2.pk = '5f85469378ebc3de6b8cf155'
    b3 = Board(title='주식, 투자')
    b3.pk = '5f85469378ebc3de6b8cf156'

    return [b1, b2, b3]


@pytest.fixture
def boards_json():
    return [{'title': '자유게시판', '_id': '5f85469378ebc3de6b8cf154', 'posts': []},
            {'title': '부동산', '_id': '5f85469378ebc3de6b8cf155', 'posts': []},
            {'title': '주식, 투자', '_id': '5f85469378ebc3de6b8cf156', 'posts': []},
            ]


@mock.patch("backend.views.boards.BoardLoadService.get_many")
def test_get_boards(mock_get_many, client, boards, boards_json):
    mock_get_many.return_value = boards

    response: JSONResponse = client.get('/boards/')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert boards_json == data


@mock.patch("backend.views.boards.BoardLoadService.get_many")
def test_get_boards_internal_server_error(mock_get_many,  client):
    mock_get_many.side_effect = RuntimeError()
    response: JSONResponse = client.get('/boards/')

    assert response.status_code == 500
    data = json.loads(response.data)
    assert data['message'] == 'Internal Server Error'
