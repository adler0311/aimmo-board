from backend.models.post import Post
from mongoengine import connect, disconnect
from bson import ObjectId
from unittest import TestCase
from mongoengine import Document, StringField


class TestPostModel(TestCase):
    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_init(self):
        data = {'title': '제목', 'content': '내용', 'writer': '작성자'}
        p = Post(**data)

        assert p is not None
        assert p.title == data['title']

    def test_objects_get_by__id(self):
        result = Post.objects().get(pk='5f866890b99bca3d269bdd8f')

        assert result is not None
        assert type(result) is Post

    def test_objects_update(self):
        data = {'title': '제목', 'content': '내용', 'writer': '작성자'}
        p = Post(**data)
        p.save()
        p = Post.objects().first()
        assert p.title == '제목'

        id = p.id
        result = Post.objects(pk=id).update_one(title="변경된 제목")

        modified = Post.objects().first()
        assert modified.title == '변경된 제목'
