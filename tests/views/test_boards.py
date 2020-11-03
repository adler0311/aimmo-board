import pytest
from flask import Response, url_for

from backend.models.board import Board
from tests.factories.board import BoardFactory


class Describe_BoardsView:
    @pytest.fixture(autouse=True)
    def tearDown(self):
        Board.objects.delete()

    class Describe_index:
        @pytest.fixture
        def boards(self):
            return BoardFactory.create_batch(20)

        @pytest.fixture
        def subject(self, client, boards):
            url = url_for('BoardsView:index')
            return client.get(url)

        def test_게시판_목록을_가져온다(self, subject: Response):
            assert subject.status_code == 200
            boards = subject.json
            assert len(boards) == 20

        class Context_게시판이_없는_경우:
            @pytest.fixture
            def boards(self):
                return None

            def test_빈_배열을_반환한다(self, subject: Response):
                assert subject.status_code == 200
                boards = subject.json
                assert type(boards) is list
                assert len(boards) == 0
