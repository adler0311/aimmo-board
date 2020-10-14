from backend.models.post import Post
from mongoengine import connect
from bson import ObjectId


def test_init():
    data = {'title': '제목', 'content': '내용', 'writer': '작성자'}
    p = Post(**data)

    assert p is not None
    assert p.title == data['title']


def test_objects_get_by__id():
    connect('test')
    result = Post.objects().get(pk='5f866890b99bca3d269bdd8f')

    assert result is not None
    assert type(result) is Post
