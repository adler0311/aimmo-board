from typing import List

import pytest
from bson import ObjectId
from flask import url_for

from backend.shared.post_order_type import PostOrderType
from tests.factories.board import BoardFactory
from tests.factories.post import PostFactory
import json


class Describe_PostsView:
    @pytest.fixture
    def board(self):
        return BoardFactory.create(title='parker')

    @pytest.fixture
    def url(self, board):
        return url_for('PostsView:post', board_id=board.id)

    class Describe_get_board_posts:
        @pytest.fixture
        def params(self):
            return None

        @pytest.fixture
        def posts(self, board):
            return PostFactory.create_batch(20, board=board)

        @pytest.fixture
        def board_id(self, board):
            return board.id

        @pytest.fixture
        def subject(self, client, board_id, posts, params):
            url = url_for('PostsView:get_board_posts', board_id=board_id)
            return client.get(url, query_string=params)

        def test_post_목록을_가져온다(self, subject, posts):
            assert subject.status_code == 200
            assert len(subject.json) == 20

        class Context_board가_없는_경우:
            @pytest.fixture
            def board_id(self):
                return ObjectId()

            def test_404를_반환한다(self, subject):
                assert subject.status_code == 404

        class Context_order_type이_유효하지_않은_경우:
            @pytest.fixture
            def params(self):
                return {'order_type': 'some_invalid_order_type'}

            def test_422를_반환한다(self, subject):
                assert subject.status_code == 422

        class Context_order_type이_created인_경우:
            @pytest.fixture
            def params(self):
                return {'order_type': PostOrderType.CREATED.value}

            def test_200을_반환한다(self, subject):
                assert subject.status_code == 200

            def test_게시글_목록이_최신순으로_내려온다(self, subject):
                posts: List = subject.json
                for i in range(len(posts) - 1):
                    assert posts[i]['created'] > posts[i + 1]['created']

        class Context_order_type이_comment인_경우:
            @pytest.fixture
            def params(self):
                return {'order_type': PostOrderType.COMMENT.value}

            @pytest.fixture
            def posts(self, board):
                return PostFactory.create_batch_with_comments(20, board)

            def test_200을_반환한다(self, subject):
                assert subject.status_code == 200

            def test_게시글_목록이_댓글_많은_순으로_내려온다(self, subject):
                posts: List = subject.json
                for i in range(len(posts) - 1):
                    assert posts[i]['comments'] >= posts[i + 1]['comments']

        class Context_order_type이_like인_경우:
            @pytest.fixture
            def params(self):
                return {'order_type': PostOrderType.LIKE.value}

            def test_200을_반환한다(self, subject):
                assert subject.status_code == 200

            def test_게시글_목록이_좋아요_많은_순으로_내려온다(self, subject):
                posts: List = subject.json
                for i in range(len(posts) - 1):
                    assert posts[i]['likes'] >= posts[i + 1]['likes']

        class Context_limit으로_5개를_요청하는_경우:
            @pytest.fixture
            def params(self):
                return {'limit': 5}

            def test_200을_반환한다(self, subject):
                assert subject.status_code == 200

            def test_게시글_목록이_5개_내려온다(self, subject):
                posts = subject.json
                assert len(posts) == 5

        class Context_keyword값이_None이_아닌_경우:
            @pytest.fixture
            def keyword(self):
                return '검색키워드'

            @pytest.fixture
            def posts(self, board, keyword):
                return PostFactory.create_including_keyword_in_title_or_content(20, board, keyword)

            def test_200을_반환한다(self, subject):
                assert subject.status_code == 200

            def test_keyword가_제목_혹은_내용에_포함된_게시글만_내려온다(self, subject, keyword):
                posts = subject.json
                for post in posts:
                    assert keyword in post['title'] or keyword in post['content']

            class Describe_post:
                @pytest.fixture
                def headers(self, token_header):
                    return token_header

                @pytest.fixture
                def title_and_content_exist_data(self):
                    return {'title': '게시글 제목', 'content': '게시글 내용'}

                @pytest.fixture
                def request_body(self, title_and_content_exist_data):
                    return title_and_content_exist_data

                @pytest.fixture
                def subject(self, client, board, headers, request_body):
                    url = url_for('PostsView:post', board_id=board.id)
                    return client.post(url, headers=headers, data=json.dumps(request_body))

                def test_게시글을_저장하고_201을_반환한다(self, subject):
                    assert subject.status_code == 201

                class Context_토큰이_없는_경우:
                    @pytest.fixture
                    def headers(self, default_header):
                        return default_header

                    def test_401을_반환한다(self, subject):
                        assert subject.status_code == 401

                class Context_request_body_데이터에_제목이_없는_경우:
                    @pytest.fixture
                    def no_title_data(self):
                        return {'content': '게시글 내용'}

                    @pytest.fixture
                    def request_body(self, no_title_data):
                        return no_title_data

                    def test_422를_반환한다(self, subject):
                        assert subject.status_code == 422

                class Context_request_body_데이터에_내용이_없는_경우:
                    @pytest.fixture
                    def no_content_data(self):
                        return {'title': '게시글 제목'}

                    @pytest.fixture
                    def request_body(self, no_content_data):
                        return no_content_data

                    def test_422를_반환한다(self, subject):
                        assert subject.status_code == 422

            class Describe_put:
                @pytest.fixture
                def to_modify_post(self, auth_token):
                    return PostFactory.create(writer=auth_token.user)

                @pytest.fixture
                def to_put_data(self):
                    return {'title': '바뀔 게시글 제목', 'content': '바뀔 게시글 내용'}

                @pytest.fixture
                def post_id(self, to_modify_post):
                    return to_modify_post.id

                @pytest.fixture
                def request_body(self, to_put_data):
                    return to_put_data

                @pytest.fixture
                def subject(self, board, client, token_header, post_id, request_body):
                    url = url_for('PostsView:put', board_id=board.id, post_id=post_id)
                    return client.put(url, headers=token_header, data=json.dumps(request_body))

                def test_게시글을_수정하고_200을_반환한다(self, subject):
                    assert subject.status_code == 200

                class Context_게시글_제목만_request_body로_있는_경우:
                    @pytest.fixture
                    def only_have_title_to_modify_data(self):
                        return {'title': '바뀔 게시글 제목'}

                    @pytest.fixture
                    def request_body(self, only_have_title_to_modify_data):
                        return only_have_title_to_modify_data

                    def test_422를_반환한다(self, subject):
                        assert subject.status_code == 422

                class Context_수정할_게시글이_없는_경우:
                    @pytest.fixture
                    def post_id(self):
                        return ObjectId()

                    def test_404를_반환한다(self, subject):
                        assert subject.status_code == 404

                class Context_수정_권한이_없는_경우:
                    @pytest.fixture
                    def not_auth_token_user_post(self):
                        return PostFactory.create()

                    @pytest.fixture
                    def post_id(self, not_auth_token_user_post):
                        return not_auth_token_user_post.id

                    def test_403을_반환한다(self, subject):
                        assert subject.status_code == 403

            class Describe_delete:
                @pytest.fixture
                def post(self, auth_token):
                    return PostFactory.create(writer=auth_token.user)

                @pytest.fixture
                def post_id(self, post):
                    return post.id

                @pytest.fixture
                def subject(self, client, board, token_header, post_id):
                    url = url_for('PostsView:delete', board_id=board.id, post_id=post_id)
                    return client.delete(url, headers=token_header)

                def test_작성자가_본인의_게시글을_삭제하고_200을_반환한다(self, subject):
                    return subject.status_code == 200

                class Context_삭제할_게시글이_없는_경우:
                    @pytest.fixture
                    def post_id(self):
                        return ObjectId()

                    def test_404를_반환한다(self, subject):
                        return subject.status_code == 404

                class Context_삭제_권한이_없는_경우:
                    @pytest.fixture
                    def not_auth_token_user_post(self):
                        return PostFactory.create()

                    @pytest.fixture
                    def post_id(self, not_auth_token_user_post):
                        return not_auth_token_user_post.id

                    def test_403을_반환한다(self, subject):
                        assert subject.status_code == 403
