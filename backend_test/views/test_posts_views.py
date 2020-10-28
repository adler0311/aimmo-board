import pytest
import json
from unittest import mock
from pytest_flask.plugin import JSONResponse

from mongoengine import DoesNotExist
from backend.models.post import Post
from backend.models.auth_token import AuthToken
from backend.models.user import User
from backend.schemas.post_schema import PostSchema


@pytest.fixture
def posts():
    p1 = Post(title='title1', content='content1')
    p1.pk = '5f85469378ebc3de6b8cf154'
    p2 = Post(title='title2', content='content2')
    p2.pk = '5f85469378ebc3de6b8cf154'
    p3 = Post(title='title3', content='content3')
    p3.pk = '5f85469378ebc3de6b8cf154'

    return [p1, p2, p3]


@pytest.fixture
def dummy_writer():
    writer = User()
    writer.pk = 'uf85469378ebc3de6b8cf154'
    return writer


@pytest.fixture
def dummy_board_id():
    return 'dummy_board_id'


@pytest.fixture
def dummy_post_id():
    return 'dummy_post_id'


@pytest.fixture
def dummy_data():
    return {
        'title': '제목',
        'content': '내용',
    }


# @mock.patch("backend.views.posts_view.Post")
# @mock.patch("backend.views.posts_view.PostService.get_many")
# def test_get_posts(mock_get_many, mock_post, client, posts):
#     mock_get_many.return_value = posts
#
#     http_response: JSONResponse = client.get('/posts/')
#
#     assert http_response.status_code == 200
#
#     schema = PostSchema(many=True)
#     result = {'posts': schema.dump(posts)}
#     data = json.loads(http_response.data)
#     assert result == data


@mock.patch("backend.views.posts_view.PostSchema.dump")
@mock.patch("backend.views.posts_view.PostLoadService.get_many")
def test_board_posts_success(mock_get_many, mock_dump,  client, posts, dummy_board_id):
    mock_dump.return_value = {}
    mock_get_many.return_value = posts

    response: JSONResponse = client.get(
        '/boards/{}/posts/?order_type=key'.format(dummy_board_id))

    assert response.status_code == 200

    schema = PostSchema(many=True)
    result = schema.dump(posts)
    data = json.loads(response.data)
    assert result == data


@mock.patch("backend.views.decorators.AuthService.get_auth_token")
@mock.patch("backend.views.posts_view.PostSchema.load")
@mock.patch("backend.views.posts_view.PostService.post")
def test_add_post_is_authenticated(mock_post_method, mock_load, mock_get_auth_token, client,
                                   dummy_writer, dummy_board_id, valid_token_header, valid_token, dummy_data):

    mock_get_auth_token.return_value = AuthToken(token=valid_token, user=dummy_writer)
    mock_load.return_value = dummy_data
    mock_post_method.return_value = True

    response = client.post(
        '/boards/{}/posts/'.format(dummy_board_id), data=json.dumps(dummy_data), headers=valid_token_header)

    assert response.status_code == 201


def test_add_post_empty_token(client, dummy_board_id, dummy_data, default_header):

    response = client.post(
        '/boards/{}/posts/'.format(dummy_board_id), data=json.dumps(dummy_data), headers=default_header)

    assert response.status_code == 401


@mock.patch("backend.views.decorators.AuthService.get_auth_token")
def test_add_post_not_authenticated(mock_get_auth_token, client, dummy_board_id, dummy_data, invalid_token_header):
    mock_get_auth_token.side_effect = DoesNotExist()

    response = client.post(
        '/boards/{}/posts/'.format(dummy_board_id), data=json.dumps(dummy_data), headers=invalid_token_header)

    assert response.status_code == 401


@mock.patch("backend.views.decorators.AuthService.get_auth_token")
@mock.patch("backend.views.posts_view.PostService.post")
def test_add_post_redundant_JSON_field(mock_post, mock_get_auth_token, client,
                                       dummy_board_id, valid_token_header):

    mock_get_auth_token.return_value = AuthToken()
    mock_post.return_value = True

    data = {
        'title': '제목',
        'content': '내용',
        'redundant_field': '댓글 입니다'
    }

    response = client.post(
        '/boards/{}/posts/'.format(dummy_board_id), data=json.dumps(data), headers=valid_token_header)

    assert response.status_code == 201


@mock.patch("backend.views.decorators.AuthService.get_auth_token")
@mock.patch("backend.views.posts_view.PostService.update")
def test_add_post_insufficient_JSON_field(mock_update, mock_get_auth_token, client,
                                          dummy_board_id, valid_token_header):
    mock_update.return_value = False

    data = {
        'title': '제목',
    }

    response = client.post(
        '/boards/{}/posts/'.format(dummy_board_id), data=json.dumps(data), headers=valid_token_header)

    assert response.status_code == 422


# @mock.patch("backend.views.posts_view.Post")
# def test_get_post_which_not_exist_id(mock_post, client):
#     mock_post.objects.get.side_effect = DoesNotExist()
#     invalid_post_id = '5f85469378ebc3de6b8cf152'
#
#     http_response = client.get('/posts/{}/'.format(invalid_post_id))
#
#     assert http_response.status_code == 404

@mock.patch("backend.views.decorators.AuthService.get_auth_token")
@mock.patch("backend.views.posts_view.PostService.is_writer")
def test_put_not_authorized(mock_is_writer, mock_get_auth_token, client,
                            dummy_board_id, dummy_data, valid_token, valid_token_header, dummy_post_id):

    not_writer = User()
    mock_get_auth_token.return_value = AuthToken(token=valid_token, user=not_writer)
    mock_is_writer.return_value = False

    response = client.put(
        '/boards/{}/posts/{}'.format(dummy_board_id, dummy_post_id), data=json.dumps(dummy_data), headers=valid_token_header)

    assert response.status_code == 403


@mock.patch("backend.views.decorators.AuthService.get_auth_token")
@mock.patch("backend.views.posts_view.PostService.update")
@mock.patch("backend.views.posts_view.PostService.is_writer")
def test_put_has_failed(mock_is_writer, mock_update, mock_get_auth_token, client, dummy_board_id,
                        valid_token, valid_token_header, dummy_data, dummy_post_id):
    writer = User()
    mock_get_auth_token.return_value = AuthToken(token=valid_token, user=writer)
    mock_is_writer.return_value = True
    mock_update.return_value = False

    response = client.put(
        '/boards/{}/posts/{}'.format(dummy_board_id, dummy_post_id), data=json.dumps(dummy_data), headers=valid_token_header)

    assert response.status_code == 404


@mock.patch("backend.views.decorators.AuthService.get_auth_token")
@mock.patch("backend.views.posts_view.PostService.update")
@mock.patch("backend.views.posts_view.PostService.is_writer")
def test_put_is_success(mock_is_writer, mock_update, mock_get_auth_token, client,
                           dummy_board_id, valid_token, valid_token_header, dummy_data, dummy_post_id):
    writer = User()
    mock_get_auth_token.return_value = AuthToken(token=valid_token, user=writer)
    mock_is_writer.return_value = True
    mock_update.return_value = True

    response = client.put(
        '/boards/{}/posts/{}'.format(dummy_board_id, dummy_post_id), data=json.dumps(dummy_data), headers=valid_token_header)

    assert response.status_code == 200


def test_delete_post_empty_token(client, dummy_board_id, dummy_post_id):

    response = client.delete(
        '/boards/{}/posts/{}'.format(dummy_board_id, dummy_post_id))

    assert response.status_code == 401


@mock.patch("backend.views.decorators.AuthService.get_auth_token")
def test_delete_post_not_authenticated(mock_get_auth_token, client,
                                       dummy_board_id, dummy_post_id, invalid_token_header):
    mock_get_auth_token.side_effect = DoesNotExist()

    response = client.delete(
        '/boards/{}/posts/{}'.format(dummy_board_id, dummy_post_id), headers=invalid_token_header)

    assert response.status_code == 401


@mock.patch("backend.views.decorators.AuthService.get_auth_token")
@mock.patch("backend.views.posts_view.PostService.is_writer")
def test_delete_post_not_authorized(mock_is_writer, mock_get_auth_token, client,
                                    dummy_board_id, valid_token, valid_token_header, dummy_data, dummy_post_id):

    not_writer = User()
    mock_get_auth_token.return_value = AuthToken(token=valid_token, user=not_writer)

    mock_is_writer.return_value = False

    response = client.delete(
        '/boards/{}/posts/{}'.format(dummy_board_id, dummy_post_id), data=json.dumps(dummy_data), headers=valid_token_header)

    assert response.status_code == 403


@mock.patch("backend.views.decorators.AuthService.get_auth_token")
@mock.patch("backend.views.posts_view.PostService.is_writer")
@mock.patch("backend.views.posts_view.PostService.delete")
def test_delete_post_is_authorized(mock_delete, mock_is_writer, mock_get_auth_token, client,
                                   dummy_board_id, valid_token, valid_token_header, dummy_post_id):

    writer = User()
    mock_is_writer.return_value = True
    mock_delete.return_value = True
    mock_get_auth_token.return_value = AuthToken(token=valid_token, user=writer)

    response = client.delete(
        '/boards/{}/posts/{}'.format(dummy_board_id, dummy_post_id),  headers=valid_token_header)

    assert response.status_code == 200


