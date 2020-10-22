import pytest
from unittest import mock
from backend.models.auth_token import AuthToken
import json


@pytest.fixture
def valid_token():
    return 'valid_token'


@pytest.fixture
def valid_token_headers(valid_token):
    return {'Authorization': valid_token, 'ContentType': 'application/json'}


@pytest.fixture
def dummy_query_data():
    return {'contentId': 'dummy_content_id', 'contentType': 'post'}


# @mock.patch("backend.views.likes_view.LikeService.get_likes")
# def test_get_likes_of_content_not_exist(mock_get_likes, client,
#                                         valid_token_headers, valid_token, dummy_query_data):

#     mock_get_likes.return_value = False

#     response = client.get(
#         '/likes?contentId={}&contentType={}'.format(
#             dummy_query_data['contentId'], dummy_query_data['contentType']),
#         headers=valid_token_headers)

#     assert response.status_code == 404


@mock.patch("backend.views.likes_view.LikeService.get_likes")
@mock.patch("backend.views.likes_view.LikeSchema.dump")
def test_get_likes_success(mock_dump, mock_get_post_like,
                           client, valid_token,
                           valid_token_headers, dummy_query_data):

    mock_get_post_like.return_value = True
    mock_dump.return_value = True

    response = client.get(
        '/likes?contentId={}&contentType={}'.format(
            dummy_query_data['contentId'], dummy_query_data['contentType']),
        headers=valid_token_headers)

    assert response.status_code == 200


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.likes_view.LikeService.post_like")
def test_create_like_of_content_success(mock_post_like, mock_auth_token, client,
                                        dummy_query_data, valid_token_headers):

    mock_auth_token.objects.get.return_value = AuthToken(token=valid_token)
    mock_post_like.return_value = True

    response = client.post('/likes/', data=json.dumps(dummy_query_data),
                           headers=valid_token_headers)

    assert response.status_code == 201


def test_create_post_like_success(client):
    NotImplemented
