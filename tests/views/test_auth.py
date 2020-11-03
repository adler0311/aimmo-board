import json

import pytest
from flask import Response, url_for

from backend.models.auth_token import AuthToken
from backend.utils import Utils
from tests.factories.user import UserFactory


class Describe_AuthView:
    class Describe_get:
        @pytest.fixture
        def subject(self, client, token_header):
            url = url_for('AuthView:get')
            return client.get(url, headers=token_header)

        def test_200을_반환한다(self, subject: Response):
            assert subject.status_code == 200

        def test_토큰을_반환한다(self, subject: Response, auth_token: AuthToken):
            data = subject.json
            assert data['token'] == auth_token.token

    class Describe_post:
        @pytest.fixture
        def password(self):
            return 'pass123'

        @pytest.fixture
        def user(self, password):
            return UserFactory.create(password=Utils.encrypt_password(password))

        @pytest.fixture
        def request_body(self, user, password):
            return {'userId': user.user_id, 'password': password}

        @pytest.fixture
        def subject(self, client, request_body, default_header):
            url = url_for('AuthView:post')
            return client.post(url, headers=default_header, data=json.dumps(request_body))

        def test_201을_반환한다(self, subject: Response):
            assert subject.status_code == 201

        def test_토큰을_반환한다(self, subject: Response):
            data = subject.json
            assert data['token'] is not None

        class Context_아이디와_비밀번호에_매칭되는_유저가_없는_경우:
            @pytest.fixture
            def request_body(self, user):
                return {'userId': user.user_id, 'password': '틀린 비밀번호'}

            def test_404를_반환한다(self, subject):
                assert subject.status_code == 404
