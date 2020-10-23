from bson.json_util import default
import pytest
from backend.app import create_app


@pytest.fixture(scope='function')
def app():
    yield create_app()


@pytest.fixture
def valid_token():
    return 'valid_token'


@pytest.fixture
def invalid_token():
    return 'invalid_token'


@pytest.fixture
def default_header():
    return {'Content-Type': 'application/json'}


@pytest.fixture
def valid_token_header(valid_token, default_header):
    return dict(default_header, **{'Authorization': valid_token})


@pytest.fixture
def invalid_token_header(invalid_token, default_header):
    return dict(default_header, **{'Authorization': invalid_token})


@pytest.fixture
def not_writer_token_header(default_header):
    return dict(default_header, **{'Authorization': 'not_writer'})


@pytest.fixture
def writer_token_header(default_header):
    return dict(default_header, **{'Authorization': 'writer'})
