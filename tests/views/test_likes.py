import json
from typing import List

import pytest
from flask import Response, url_for

from backend.models.like import Like
from backend.shared.content_type import ContentType
from tests.factories.like import LikeFactory
from tests.factories.post import PostFactory


class Describe_LikesView:
    @pytest.fixture
    def post(self):
        return PostFactory.create()

    @pytest.fixture
    def likes(self, post, auth_token):
        return LikeFactory.create_batch_with_content_post(20, content_id=str(post.id), user=auth_token.user)

    class Describe_index:
        @pytest.fixture
        def params(self, likes: List[Like]):
            return {'contentId': likes[0].content_id, 'contentType': ContentType.POST.value}

        @pytest.fixture
        def subject(self, client, params):
            url = url_for('LikesView:index')
            return client.get(url, query_string=params)

        def test_200을_반환한다(self, subject: Response):
            assert subject.status_code == 200

        def test_좋아요_목록을_반환한다(self, subject: Response):
            data = subject.json
            assert len(data) == 20

        class Context_content_id가_없는_경우:
            @pytest.fixture
            def params(self):
                return {'contentType': ContentType.POST.value}

            def test_422를_반환한다(self, subject):
                assert subject.status_code == 422

        class Context_content_type이_없는_경우:
            @pytest.fixture
            def params(self, likes: List[Like]):
                return {'contentId': likes[0].content_id}

            def test_422를_반환한다(self, subject):
                assert subject.status_code == 422

    class Describe_post:
        @pytest.fixture
        def headers(self, token_header):
            return token_header

        @pytest.fixture
        def request_body(self, likes):
            return {'contentId': likes[0].content_id, 'contentType': ContentType.POST.value}

        @pytest.fixture
        def subject(self, client, headers, request_body):
            url = url_for('LikesView:post')
            return client.post(url, headers=headers, data=json.dumps(request_body))

        def test_201을_반환한다(self, subject: Response):
            assert subject.status_code == 201

        class Context_토큰이_없는_경우:
            @pytest.fixture
            def headers(self, default_header):
                return default_header

            def test_401을_반환한다(self, subject: Response):
                assert subject.status_code == 401

    class Describe_delete:
        @pytest.fixture
        def headers(self, token_header):
            return token_header

        @pytest.fixture
        def request_body(self, likes):
            return {'contentId': likes[0].content_id, 'contentType': ContentType.POST.value}

        @pytest.fixture
        def subject(self, client, headers, request_body):
            url = url_for('LikesView:delete')
            return client.delete(url, headers=headers, data=json.dumps(request_body))

        def test_200을_반환한다(self, subject: Response):
            assert subject.status_code == 200

        class Context_토큰이_없는_경우:
            @pytest.fixture
            def headers(self, default_header):
                return default_header

            def test_401을_반환한다(self, subject: Response):
                assert subject.status_code == 401
