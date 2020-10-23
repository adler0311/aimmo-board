
from mongoengine import connect, disconnect
from mongoengine.queryset.visitor import Q
from unittest import TestCase
from backend.models.user import User


class TestUserModel(TestCase):

    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')
        cls.dummy_user = User(user_id='id132', password='pw123')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_init(self):
        assert self.dummy_user is not None
        assert self.dummy_user.user_id == 'id132'

    def test_save(self):
        data = {'user_id': 'id132', 'password': 'pw123'}
        u = User(**data)
        u.save()

        saved_u = User.objects.first()

        assert saved_u is not None
        assert saved_u.user_id == 'id132'

    def test_filter_multiple_key(self):
        data = {'user_id': 'id132', 'password': 'pw123'}
        u = User(**data)
        u.save()

        saved_u = User.objects(Q(user_id='id132') &
                               Q(password='pw123')).first()

        assert saved_u is not None
        assert saved_u.user_id == 'id132'

    def test_filter_multiple_key_but_not_exist(self):
        self.dummy_user.save()

        saved_u = User.objects(Q(user_id='id') &
                               Q(password='pw123')).first()

        assert saved_u is None

    def test_get_user_by_id_and_password_found(self):
        self.dummy_user.save()

        u = User.get_user_by_id_and_password(user_id='id132', password='pw123')
        assert u is not None
