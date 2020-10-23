from bson import ObjectId
from unittest import TestCase
from mongoengine import connect, disconnect

from backend.models.user import User
from backend.models.comment import Comment

import pytest


@pytest.fixture(scope='class')
def comments(request):
    u = User()
    saved = u.save()
    c = {'content': '댓글입니다', 'post_id': ObjectId(
        '5f85469378ebc3de6b8cf154'), 'writer': u}
    request.cls.comments = [c]


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

    def test_put_comment_by_post_id(self):
        Comment.objects.insert([Comment(**c) for c in self.comments])
        c: Comment = Comment.objects.first()

        result = Comment.objects(id=c.pk).update_one(content="업데이트 내용")

        assert result == 1
        assert Comment.objects.get(id=c.pk).content == "업데이트 내용"

    def test_delete_comment_by_post_id(self):
        Comment.objects.insert([Comment(**c) for c in self.comments])
        c: Comment = Comment.objects.first()

        result = Comment.objects(id=c.pk).delete()

        assert result == 1
        comments = Comment.objects(id=c.pk)
        assert len(comments) == 0

    def test_writer_type_is_user(self):
        c = self.comments[0]
        comment = Comment(**c)
        result = comment.save()

        assert result.writer is not None
        assert type(result.writer) is User
