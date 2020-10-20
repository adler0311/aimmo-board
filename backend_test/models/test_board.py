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
