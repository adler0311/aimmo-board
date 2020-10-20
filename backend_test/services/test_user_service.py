from backend.services.user_service import UserService
from unittest import mock


@mock.patch("backend.services.user_service.User")
@mock.patch("backend.services.user_service.AuthToken")
def test_signup(mock_auth_token, mock_user):
    service = UserService()
    data = {'userId': 'new user', 'password': '123123'}

    result = service.signup(data)
    assert result is not None
