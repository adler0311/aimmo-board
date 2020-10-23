
from mongoengine import connect, disconnect
from unittest import TestCase
from backend.models.auth_token import AuthToken
from backend.models.user import User


class TestAuthTokenModel(TestCase):
    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_init(self):
        u = User(user_id='id132', password='pw123')
        at = AuthToken(token='aaaa', user=u)

        assert at is not None

    def test_save_with_user(self):
        u = User(user_id='id132', password='pw123')
        u.save()

        at = AuthToken(token='aaaa', user=u)
        at.save()

        saved_at = AuthToken.objects.first()

        assert saved_at is not None
        assert saved_at.user.user_id == 'id132'
