
from mongoengine import connect, disconnect
from mongoengine.queryset.visitor import Q
from bson import ObjectId
from unittest import TestCase
from mongoengine import Document, StringField
from backend.models.user import User


class TestUserModel(TestCase):
    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_init(self):
        data = {'user_id': 'id132', 'password': 'pw123'}
        u = User(**data)

        assert u is not None
        assert u.user_id == 'id132'

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
        data = {'user_id': 'id132', 'password': 'pw123'}
        u = User(**data)
        u.save()

        saved_u = User.objects(Q(user_id='id') &
                               Q(password='pw123')).first()

        assert saved_u is None
