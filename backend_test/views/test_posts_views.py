import pytest
import json
from unittest import mock
from pytest_flask.plugin import JSONResponse
from bson import ObjectId
from mongoengine import DoesNotExist
from backend.models.post import Post
from backend.schemas.post_schema import PostSchema


@pytest.fixture
def posts():
    p1 = Post(title='title1', content='content1', writer='writer1')
    p1.pk = '5f85469378ebc3de6b8cf154'
    p2 = Post(title='title2', content='content2', writer='writer2')
    p2.pk = '5f85469378ebc3de6b8cf154'
    p3 = Post(title='title3', content='content3', writer='writer3')
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
def test_add_post(mock_post, client):
    headers = {'Content-Type': 'application/json'}
    data = {
        'title': '제목',
        'content': '내용',
        'writer': '작성자'
    }

    response = client.post('/posts/', data=json.dumps(data), headers=headers)

    assert response.status_code == 201


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


@mock.patch("backend.views.posts_view.Post")
def test_put_post(mock_post, client, posts):
    p = posts[0]

    headers = {'Content-Type': 'application/json'}
    data = {
        'title': '제목',
        'content': '내용',
        'writer': '작성자'
    }

    response = client.put(
        '/posts/{}/'.format(p['_id']), data=json.dumps(data), headers=headers)

    assert response.status_code == 200


@mock.patch("backend.views.posts_view.Post")
def test_delete_post(mock_post, client, posts):
    p = posts[0]
    response = client.delete('/posts/{}/'.format(p['_id']))

    assert response.status_code == 200


@mock.patch("backend.views.posts_view.Post")
def test_delete_which_not_exist(mock_post, client, posts):
    objects = mock_post.objects()
    objects.delete.return_value = 0

    p = posts[0]
    response = client.delete('/posts/{}/'.format(p['_id']))

    assert response.status_code == 404
