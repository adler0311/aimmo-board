from unittest import mock

import pytest

from backend.models.auth_token import AuthToken
from tests.factories.auth_token import AuthTokenFactory


@pytest.fixture(scope="session")
def app():
    from backend.app import create_app
    app = create_app()
    return app


@pytest.fixture(scope="session", autouse=True)
def app_context(app):
    ctx = app.app_context()
    ctx.push()
    yield
    ctx.pop()


@pytest.fixture(scope='session', autouse=True)
def db(app):
    import mongoengine
    conn = mongoengine.connect(host=app.config['MONGO_URI'])
    yield conn
    mongoengine.disconnect()


@pytest.fixture
def client(app):
    app.testing = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def default_header():
    return {'Content-Type': 'application/json'}


@pytest.fixture
def auth_token():
    return AuthTokenFactory.create()


@pytest.fixture
def token_header(auth_token: AuthToken, default_header: dict):
    return dict({'Authorization': auth_token.token}, **default_header)
