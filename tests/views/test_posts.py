import logging

import pytest
from bson import ObjectId
from flask import url_for

from tests.factories.board import BoardFactory
from tests.factories.post import PostFactory


class Describe_PostsView:
    class Describe_get_board_posts:
        @pytest.fixture
        def board(self):
            return BoardFactory.create(title='parker')

        @pytest.fixture
        def posts(self, board):
            return PostFactory.create_batch(20, board=board)

        @pytest.fixture
        def subject(self, client, board, posts):
            url = url_for('PostsView:get_board_posts', board_id=board.id)
            return client.get(url)

        def test_post_목록을_가져온다(self, subject, posts):
            assert subject.status_code == 200
            assert len(subject.json) == 20

        class Context_board가_없는_경우:
            @pytest.fixture
            def subject(self, client, board, posts):
                url = url_for('PostsView:get_board_posts', board_id=ObjectId())
                return client.get(url)

            def test_404를_반환한다(self, subject):
                assert subject.status_code == 404
