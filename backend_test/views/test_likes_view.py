from backend.models.post import Post
import pytest
from unittest import mock
from backend.models.auth_token import AuthToken
import json


@pytest.fixture
def dummy_query_data():
    return {'contentId': 'dummy_content_id', 'contentType': 'post'}


@mock.patch("backend.views.likes_view.LikeService.get_many")
@mock.patch("backend.views.likes_view.LikeSchema.dump")
def test_get_likes_success(mock_dump, mock_get_many,
                           client, valid_token_header, dummy_query_data):

    mock_get_many.return_value = [Post()]
    mock_dump.return_value = True

    response = client.get(
        '/likes/?contentId={}&contentType={}'.format(
            dummy_query_data['contentId'], dummy_query_data['contentType']),
        headers=valid_token_header)

    assert response.status_code == 200


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.likes_view.LikeService.post")
def test_create_like_of_content_success(mock_post, mock_auth_token, client,
                                        dummy_query_data, valid_token, valid_token_header):

    mock_auth_token.objects.get.return_value = AuthToken(token=valid_token)
    mock_post.return_value = True

    response = client.post('/likes/', data=json.dumps(dummy_query_data),
                           headers=valid_token_header)

    assert response.status_code == 201
