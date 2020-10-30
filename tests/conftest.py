from unittest import mock

import pytest


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


@pytest.fixture(scope='function', autouse=True)
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
