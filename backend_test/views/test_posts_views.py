import pytest
import json
from unittest import mock
from pytest_flask.plugin import JSONResponse
from bson import ObjectId


@pytest.fixture
def posts():
    return [{'_id': "5f85469378ebc3de6b8cf154", 'title': 'title1', 'content': 'content1'},
            {'_id': "5f85469378ebc3de6b8cf155", 'title': 'title2', 'content': 'content2'},
            {'_id': "5f85469378ebc3de6b8cf156", 'title': 'title3', 'content': 'content3'}]


@mock.patch("backend.views.posts_view.Post")
def test_get_posts(mock_post, client, posts):
    mock_post.objects.return_value = posts

    http_response: JSONResponse = client.get('/posts/')

    assert http_response.status_code == 200

    result = {'posts': posts}
    data = json.loads(http_response.data)
    assert result == data
