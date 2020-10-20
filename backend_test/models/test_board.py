from backend.models.post import Post
from backend.models.user import User
from mongoengine import connect, disconnect
from unittest import TestCase
from backend.models.board import Board


class TestPostModel(TestCase):
    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_init(self):
        data = {'title': '자유게시판'}
        b = Board(**data)

        assert b is not None
        assert b.title == data['title']

    def test_save_with_post_with_writer(self):
        writer = User(user_id='작성자')
        writer.save()
        post = Post(writer=writer)
        post.save()
        board = Board(posts=[post])
        board.save()

        b = Board.objects.first()
        assert b is not None
        assert b.posts[0].writer is not None
        assert b.posts[0].writer.user_id == '작성자'
