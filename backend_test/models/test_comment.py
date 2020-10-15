from bson import ObjectId
from unittest import TestCase
from mongoengine import connect, disconnect, Document, StringField

from backend.models.post import Post
from backend.models.comment import Comment

import pytest


@pytest.fixture(scope='class')
def comments(request):
    comments = []
    c = {'content': '댓글입니다', 'writer': '작성자',
         'post_id': ObjectId('5f85469378ebc3de6b8cf154')}
    comments.append(c)

    request.cls.comments = comments


@pytest.mark.usefixtures("comments")
class TestCommentModel(TestCase):

    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_init(self):
        data = {'content': '댓글입니다', 'writer': '작성자'}
        c = Comment(**data)

        assert c is not None
        assert c.content == data['content']

    def test_get_comments_by_post_id(self):
        Comment.objects.insert([Comment(**c) for c in self.comments])

        comment = Comment.objects(post_id='5f85469378ebc3de6b8cf154')

        assert len(comment) > 0
