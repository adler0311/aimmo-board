from backend.models.post import Post
from backend.models.user import User
from mongoengine import connect, disconnect
from bson import ObjectId
from unittest import TestCase
from mongoengine import Document, StringField
import datetime


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
        data = {'title': '제목', 'content': '내용', 'writer': '작성자'}
        p = Post(**data)
        p.save()
        p = Post.objects().first()
        assert p.title == '제목'

        id = p.id

        result = Post.objects().get(pk=id)

        assert result is not None
        assert type(result) is Post
        assert p.title == '제목'

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

    def test_delete(self):
        data = {'title': '제목', 'content': '내용', 'writer': '작성자'}
        p = Post(**data)
        p.save()
        p = Post.objects().first()
        assert p.title == '제목'

        id = p.id
        result = Post.objects(pk=id).delete()

        assert len(Post.objects) == 0

    def test_filter_post_user(self):
        u = User()
        saved_u = u.save()

        p = Post(writer=u, title="게시글")
        saved_p = p.save()

        filtered = Post.objects(writer=saved_u.pk).get()
        assert filtered is not None
        assert filtered.title == '게시글'

    def test_datetime_field_exist(self):
        p = Post(title="게시글")
        p.save()

        now = datetime.datetime.now()
        diff_in_minute = abs((p.created - now).total_seconds() / 60)

        assert p.created is not None
        assert diff_in_minute < 1

    def test_has_writer_field(self):
        writer = User(user_id='작성자')
        writer.save()
        p = Post(title='게시글', writer=writer)
        p.save()

        p = Post.objects.first()
        assert p.title == '게시글'
        assert p.writer.user_id == '작성자'
