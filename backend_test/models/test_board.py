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

    def test_exclude_post(self):
        p1 = Post()
        saved_p1 = p1.save()
        p2 = Post()
        saved_p2 = p2.save()
        board = Board(posts=[p1, p2])
        saved_b = board.save()

        result = Board.exclude_post(saved_b.id, saved_p1.id)

        assert result == 1
        b = Board.objects.first()
        assert len(b.posts) == 1
        assert b.posts[0].id == saved_p2.id

    def test_add_post(self):
        p1 = Post()
        saved_p1 = p1.save()
        board = Board()
        saved_b = board.save()

        result = Board.add_post(saved_b.id, saved_p1.id)

        assert result == 1
        b = Board.objects.first()
        assert len(b.posts) == 1
        assert b.posts[0].id == saved_p1.id
