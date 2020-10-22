from backend.models.user import User
import pytest
from unittest import mock

from backend.models.like import Like
from backend.services.like_service import LikeService


@pytest.fixture
def dummy_content_id():
    return 'dummy_content_id'


@pytest.fixture
def dummy_content_type():
    return 'p'


# def test_get_likes(dummy_content_id, dummy_content_type):
#     like_service = LikeService()

#     assert like_service is not None

#     result = like_service.get_likes(dummy_content_id, dummy_content_type)
#     assert result is not None
