import json
from typing import List

import pytest
from bson import ObjectId
from flask import Response, url_for

from backend.models.auth_token import AuthToken
from backend.models.like import Like
from tests.factories.like import LikeFactory
from tests.factories.post import PostFactory
from tests.factories.user import UserFactory


class Describe_UsersView:
    class Describe_post:
        @pytest.fixture
        def request_body(self):
            return {'userId': 'id123', 'password': 'pw123'}

        @pytest.fixture
        def headers(self, default_header):
            return default_header

        @pytest.fixture
        def subject(self, client, request_body, headers):
            url = url_for('UsersView:post')
            return client.post(url, data=json.dumps(request_body), headers=headers)

        def test_201을_반환한다(self, subject: Response):
            assert subject.status_code == 201

        def test_응답_데이터에_토큰을_제공한다(self, subject: Response):
            data = subject.json
            assert data['token'] is not None

    class Describe_get_user_posts:
        @pytest.fixture
        def params(self):
            return None

        @pytest.fixture
        def headers(self, token_header):
            return token_header

        @pytest.fixture
        def subject(self, client, headers, params):
            url = url_for('UsersView:get_user_posts')
            return client.get(url, headers=headers, query_string=params)

        class Context_작성글을_요청하는_경우:
            @pytest.fixture
            def params(self):
                return {'type': 'write'}

            def test_200을_반환한다(self, subject: Response):
                assert subject.status_code == 200

            def test_작성자가_전부_요청하는_유저인_게시글_목록을_반환한다(self, subject: Response, auth_token: AuthToken):
                posts = subject.json
                for post in posts:
                    assert post['writer']['userId'] == auth_token.user.id

        class Context_좋아요_한_글을_요청하는_경우:
            @pytest.fixture
            def posts(self, auth_token: AuthToken):
                return PostFactory.create_batch(20, writer=auth_token.user)

            @pytest.fixture
            def likes(self, posts):
                return LikeFactory.create_like_with_post_list(posts)

            @pytest.fixture
            def params(self):
                return {'type': 'like'}

            def test_200을_반환한다(self, subject: Response):
                assert subject.status_code == 200

            def test_요청한_유저가_좋아요_한_게시글_목록을_반환한다(self, subject: Response, auth_token: AuthToken, likes: List[Like]):
                posts = subject.json
                for post in posts:
                    assert all(likes_of_post.user.id == auth_token.user.id for likes_of_post in filter(lambda l: l.content_id == post.id, likes))

        class Context_토큰이_없는_경우:
            @pytest.fixture
            def headers(self, default_header):
                return default_header

            def test_401을_반환한다(self, subject: Response):
                assert subject.status_code == 401

    class Describe_get_user_comments:
        @pytest.fixture
        def headers(self, token_header):
            return token_header

        @pytest.fixture
        def subject(self, client, headers):
            url = url_for('UsersView:get_user_comments')
            return client.get(url, headers=headers)

        def test_200을_반환한다(self, subject: Response):
            assert subject.status_code == 200

        class Context_토큰이_없는_경우:
            @pytest.fixture
            def headers(self, default_header):
                return default_header

            def test_401을_반환한다(self, subject: Response):
                assert subject.status_code == 401

    class Describe_get:
        @pytest.fixture
        def user(self):
            return UserFactory.create(user_id='테스트 유저')

        @pytest.fixture
        def user_id(self, user):
            return user.user_id

        @pytest.fixture
        def subject(self, client, user_id):
            url = url_for('UsersView:get', user_id=user_id)
            return client.get(url)

        def test_200을_반환한다(self, subject):
            assert subject.status_code == 200

        class Context_유저가_없는_경우:
            @pytest.fixture
            def user_id(self):
                return ObjectId()

            def test_404를_반환한다(self, subject):
                assert subject.status_code == 404
