import pytest
from backend.app import create_app


@pytest.fixture(scope='function')
def app():
    yield create_app()
