from unittest import TestCase

from backend.models.comment import Comment


class TestCommentModel(TestCase):
    def test_init(self):
        data = {'content': '댓글입니다', 'writer': '작성자'}
        c = Comment(**data)

        assert c is not None
        assert c.content == data['content']
