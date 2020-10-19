import pytest
import json
from unittest import mock
from pytest_flask.plugin import JSONResponse
from bson import ObjectId
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


@mock.patch("backend.views.posts_view.Post")
def test_get_posts(mock_post, client, posts):
    mock_post.objects.return_value = posts

    http_response: JSONResponse = client.get('/posts/')

    assert http_response.status_code == 200

    schema = PostSchema(many=True)
    result = {'posts': schema.dump(posts)}
    data = json.loads(http_response.data)
    assert result == data


@mock.patch("backend.views.posts_view.Post")
@mock.patch("backend.views.decorators.AuthToken")
def test_add_post_is_authenticated(mock_auth_token, mock_post, client):
    writer = User()
    writer.pk = 'uf85469378ebc3de6b8cf154'

    token = 'dummy_token'

    mock_auth_token.objects.get.return_value = AuthToken(
        token=token, user=writer)

    headers = {'Content-Type': 'application/json', 'Authorization': token}
    data = {
        'title': '제목',
        'content': '내용',
    }

    response = client.post('/posts/', data=json.dumps(data), headers=headers)

    assert response.status_code == 201


def test_add_post_empty_token(client):
    headers = {'Content-Type': 'application/json'}

    data = {
        'title': '제목',
        'content': '내용',
    }

    response = client.post('/posts/', data=json.dumps(data), headers=headers)

    assert response.status_code == 401


@mock.patch("backend.views.posts_view.Post")
@mock.patch("backend.views.decorators.AuthToken")
def test_add_post_not_authenticated(mock_auth_token, mock_post, client):
    invalid_token = 'dummy_token'

    mock_auth_token.objects.get.side_effect = DoesNotExist()

    headers = {'Content-Type': 'application/json',
               'Authorization': invalid_token}
    data = {
        'title': '제목',
        'content': '내용',
    }

    response = client.post('/posts/', data=json.dumps(data), headers=headers)

    assert response.status_code == 401


@mock.patch("backend.views.posts_view.Post")
def test_get_post(mock_post, client, posts):
    p = posts[0]
    mock_post.objects.get.return_value = p

    http_response: JSONResponse = client.get('/posts/{}/'.format(p.pk))

    assert http_response.status_code == 200
    schema = PostSchema()
    result = {'data': schema.dump(p)}
    data = json.loads(http_response.data)
    assert result == data


@mock.patch("backend.views.posts_view.Post")
def test_get_post_which_not_exist_id(mock_post, client, posts):
    mock_post.objects.get.side_effect = DoesNotExist()
    invalid_object_id = '5f85469378ebc3de6b8cf152'

    http_response = client.get('/posts/{}/'.format(invalid_object_id))

    assert http_response.status_code == 404


def test_delete_post_empty_token(client):
    dummy_post_id = '5f85469378ebc3de6b8cf154'

    response = client.delete('/posts/{}/'.format(dummy_post_id))

    assert response.status_code == 401


@mock.patch("backend.views.decorators.AuthToken")
def test_delete_post_not_authenticated(mock_auth_token, client):
    invalid_token = 'invalid_token'
    dummy_post_id = '5f85469378ebc3de6b8cf154'

    headers = {'Content-Type': 'application/json',
               'Authorization': invalid_token}

    mock_auth_token.objects.get.side_effect = DoesNotExist()

    response = client.delete(
        '/posts/{}/'.format(dummy_post_id), headers=headers)

    assert response.status_code == 401


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.posts_view.Post")
def test_delete_post_not_authorized(mock_post, mock_auth_token, client, posts):
    post_pk = 'pf85469378ebc3de6b8cf154'

    writer = User()
    writer.pk = 'uf85469378ebc3de6b8cf154'
    post = Post(writer=writer)
    post.pk = post_pk

    valid_token = 'valid_token'

    not_writer = User()
    not_writer.pk = 'uf85469378ebc3de6b8cf152'
    mock_auth_token.objects.get.return_value = AuthToken(
        token=valid_token, user=not_writer)

    objects = mock_post.objects
    objects.get.return_value = post

    headers = {'Content-Type': 'application/json',
               'Authorization': valid_token}
    data = {
        'title': '제목',
        'content': '내용'
    }

    response = client.delete(
        '/posts/{}/'.format(post_pk), data=json.dumps(data), headers=headers)

    assert response.status_code == 403


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.posts_view.Post")
def test_delete_post_is_authorized(mock_post, mock_auth_token, client, posts):
    post_pk = 'pf85469378ebc3de6b8cf154'

    writer = User()
    writer.pk = 'uf85469378ebc3de6b8cf154'
    post = Post(writer=writer)
    post.pk = post_pk

    token = 'dummy_token'

    mock_auth_token.objects.get.return_value = AuthToken(
        token=token, user=writer)
    mock_post.objects.get.return_value = post

    headers = {'Content-Type': 'application/json', 'Authorization': token}

    response = client.delete(
        '/posts/{}/'.format(post_pk),  headers=headers)

    assert response.status_code == 200


@mock.patch("backend.views.posts_view.Post")
@mock.patch("backend.views.decorators.AuthToken")
def test_add_post_not_authenticated(mock_auth_token, mock_post, client):
    invalid_token = 'dummy_token'

    mock_auth_token.objects.get.side_effect = DoesNotExist()

    headers = {'Content-Type': 'application/json',
               'Authorization': invalid_token}
    data = {
        'title': '제목',
        'content': '내용',
    }

    response = client.post('/posts/', data=json.dumps(data), headers=headers)

    assert response.status_code == 401


# @mock.patch("backend.views.decorators.AuthToken")
# def test_add_post_redundant_JSON_field(mock_auth_token, client):
#     valid_token = 'valid_token'

#     headers = {'Content-Type': 'application/json',
#                'Authorization': valid_token}
#     data = {
#         'title': '제목',
#         'content': '내용',
#         'redundant': '댓글 입니다'
#     }

#     response = client.post('/posts/', data=json.dumps(data), headers=headers)

#     assert response.status_code == 400


@mock.patch("backend.views.decorators.AuthToken")
def test_add_post_insufficient_JSON_field(mock_auth_token, client):
    valid_token = 'valid_token'

    headers = {'Content-Type': 'application/json',
               'Authorization': valid_token}
    data = {
        'title': '제목',
    }

    response = client.post('/posts/', data=json.dumps(data), headers=headers)

    assert response.status_code == 400


# @mock.patch("backend.views.posts_view.Post")
# def test_delete_post(mock_post, client, posts):
#     p = posts[0]
#     response = client.delete('/posts/{}/'.format(p['_id']))

#     assert response.status_code == 200


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.posts_view.Post")
def test_put_not_authorized(mock_post, mock_auth_token, client, posts):
    post_pk = 'pf85469378ebc3de6b8cf154'

    writer = User()
    writer.pk = 'uf85469378ebc3de6b8cf154'
    post = Post(writer=writer)
    post.pk = post_pk

    token = 'dummy_token'

    not_writer = User()
    not_writer.pk = 'uf85469378ebc3de6b8cf152'
    mock_auth_token.objects.get.return_value = AuthToken(
        token=token, user=not_writer)

    objects = mock_post.objects
    objects.get.return_value = post

    headers = {'Content-Type': 'application/json', 'Authorization': token}
    data = {
        'title': '제목',
        'content': '내용'
    }

    response = client.put(
        '/posts/{}/'.format(post_pk), data=json.dumps(data), headers=headers)

    assert response.status_code == 403


@mock.patch("backend.views.decorators.AuthToken")
@mock.patch("backend.views.posts_view.Post")
def test_put_is_authroized(mock_post, mock_auth_token, client, posts):
    post_pk = 'pf85469378ebc3de6b8cf154'

    writer = User()
    writer.pk = 'uf85469378ebc3de6b8cf154'
    post = Post(writer=writer)
    post.pk = post_pk

    token = 'dummy_token'

    mock_auth_token.objects.get.return_value = AuthToken(
        token=token, user=writer)

    objects = mock_post.objects
    objects.get.return_value = post

    headers = {'Content-Type': 'application/json', 'Authorization': token}
    data = {
        'title': '제목',
        'content': '내용',
    }

    response = client.put(
        '/posts/{}/'.format(post_pk), data=json.dumps(data), headers=headers)

    assert response.status_code == 200
