import json

import pytest
from flask import Response, url_for
from mongomock import ObjectId

from backend.models.auth_token import AuthToken
from tests.factories.auth_token import AuthTokenFactory
from tests.factories.board import BoardFactory
from tests.factories.sub_comment import CommentFactory
from tests.factories.post import PostFactory


class Describe_CommentsView:
    @pytest.fixture
    def board(self):
        return BoardFactory.create(title='default')

    @pytest.fixture
    def post(self):
        return PostFactory.create(title='default')

    @pytest.fixture
    def post_id(self, post):
        return post.id

    @pytest.fixture(autouse=True)
    def comments(self, post, auth_token: AuthToken):
        return CommentFactory.create_batch(20, post=post.id, writer=auth_token.user)

    @pytest.fixture
    def headers(self, token_header):
        return token_header

    class Describe_index:
        @pytest.fixture
        def subject(self, client, board, post_id):
            url = url_for('CommentsView:index', board_id=board.id, post_id=post_id)
            return client.get(url)

        def test_200을_반환한다(self, subject: Response):
            assert subject.status_code == 200

        def test_댓글_목록을_반환한다(self, subject: Response):
            data = subject.json
            assert len(data) == 20

        class Context_게시글이_없는_경우:
            @pytest.fixture
            def post_id(self):
                return ObjectId()

            def test_빈_목록을_반환한다(self, subject: Response):
                assert subject.status_code == 200
                data = subject.json
                assert len(data) == 0

    class Describe_get:
        @pytest.fixture
        def comment_id(self, comments):
            return comments[0].id

        @pytest.fixture
        def subject(self, client, board, post_id, comment_id):
            url = url_for('CommentsView:get', board_id=board.id, post_id=post_id, comment_id=comment_id)
            return client.get(url)

        def test_200을_반환한다(self, subject: Response):
            assert subject.status_code == 200

        class Context_댓글이_없는_경우:
            @pytest.fixture
            def comment_id(self):
                return ObjectId()

            def test_404를_반환한다(self, subject: Response):
                assert subject.status_code == 404

    class Describe_post:
        @pytest.fixture
        def request_body(self):
            return {'content': '댓글입니다'}

        @pytest.fixture
        def subject(self, client, board, post_id, headers, request_body):
            url = url_for('CommentsView:post', board_id=board.id, post_id=post_id)
            return client.post(url, headers=headers, data=json.dumps(request_body))

        def test_201을_반환한다(self, subject: Response):
            assert subject.status_code == 201

        class Context_게시글이_없는_경우:
            @pytest.fixture
            def post_id(self):
                return ObjectId()

            def test_404를_반환한다(self, subject: Response):
                assert subject.status_code == 404

        class Context_토큰이_없는_경우:
            @pytest.fixture
            def headers(self, default_header):
                return default_header

            def test_401를_반환한다(self, subject: Response):
                assert subject.status_code == 401

        class Context_댓글_내용이_없는_경우:
            @pytest.fixture
            def request_body(self):
                return {}

            def test_422를_반환한다(self, subject: Response):
                assert subject.status_code == 422

    class Describe_put:
        @pytest.fixture
        def comment_id(self, comments):
            return comments[0].id

        @pytest.fixture
        def request_body(self):
            return {'content': '수정할 댓글 내용'}

        @pytest.fixture
        def subject(self, client, board, post_id, headers, request_body, comment_id):
            url = url_for('CommentsView:put', board_id=board.id, post_id=post_id, comment_id=comment_id)
            return client.put(url, headers=headers, data=json.dumps(request_body))

        def test_200을_반환한다(self, subject: Response):
            assert subject.status_code == 200

        class Context_댓글이_없는_경우:
            @pytest.fixture
            def comment_id(self):
                return ObjectId()

            def test_404를_반환한다(self, subject: Response):
                assert subject.status_code == 404

        class Context_토큰이_없는_경우:
            @pytest.fixture
            def headers(self, default_header):
                return default_header

            def test_401를_반환한다(self, subject: Response):
                assert subject.status_code == 401

        class Context_작성자가_아닌_경우:

            @pytest.fixture
            def not_writer_auth_token(self):
                return AuthTokenFactory.create()

            @pytest.fixture
            def headers(self, default_header, not_writer_auth_token):
                return dict({'Authorization': not_writer_auth_token.token}, **default_header)

            def test_403를_반환한다(self, subject: Response):
                assert subject.status_code == 403

    class Describe_delete:
        @pytest.fixture
        def comment_id(self, comments):
            return comments[0].id

        @pytest.fixture
        def subject(self, client, board, post_id, headers, comment_id):
            url = url_for('CommentsView:delete', board_id=board.id, post_id=post_id, comment_id=comment_id)
            return client.delete(url, headers=headers)

        def test_200을_반환한다(self, subject: Response):
            assert subject.status_code == 200

        class Context_댓글이_없는_경우:
            @pytest.fixture
            def comment_id(self):
                return ObjectId()

            def test_404를_반환한다(self, subject: Response):
                assert subject.status_code == 404

        class Context_토큰이_없는_경우:
            @pytest.fixture
            def headers(self, default_header):
                return default_header

            def test_401를_반환한다(self, subject: Response):
                assert subject.status_code == 401

        class Context_작성자가_아닌_경우:
            @pytest.fixture
            def not_writer_auth_token(self):
                return AuthTokenFactory.create()

            @pytest.fixture
            def headers(self, default_header, not_writer_auth_token):
                return dict({'Authorization': not_writer_auth_token.token}, **default_header)

            def test_403를_반환한다(self, subject: Response):
                assert subject.status_code == 403
