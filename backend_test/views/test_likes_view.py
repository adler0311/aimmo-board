from typing import List

from backend.models.like import Like
from backend.models.post import Post
import pytest
from unittest import mock
from backend.models.auth_token import AuthToken
import json


@pytest.fixture
def dummy_query_data():
    return {'contentId': 'dummy_content_id', 'contentType': 'post'}


@pytest.fixture
def dummy_content_id(dummy_query_data):
    return dummy_query_data['contentId']


@pytest.fixture
def dummy_content_type(dummy_query_data):
    return dummy_query_data['contentType']


@mock.patch("backend.views.likes_view.LikeService.get_many")
def test_get_likes_is_success(mock_get_many, client, dummy_content_id, dummy_content_type):
    mock_get_many.return_value = [Like(content_id=dummy_content_id,content_type=dummy_content_type)]

    response = client.get('/likes/?contentId={}&contentType={}'.format(dummy_content_id, dummy_content_type))

    assert response.status_code == 200
    data: List[Like] = json.loads(response.data)
    assert data[0]['contentId'] == dummy_content_id


@mock.patch("backend.views.decorators.AuthService.get_auth_token")
@mock.patch("backend.views.likes_view.LikeService.post")
def test_create_like_of_content_success(mock_post, mock_get_auth_token, client,
                                        dummy_query_data, valid_token, valid_token_header):

    mock_get_auth_token.return_value = AuthToken(token=valid_token)
    mock_post.return_value = True

    response = client.post('/likes/', data=json.dumps(dummy_query_data),
                           headers=valid_token_header)

    assert response.status_code == 201
