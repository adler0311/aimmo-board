from backend.schemas.user_schema import UserSchema
from backend.models.user import User


def test_load():
    schema = UserSchema()
    data = {'userId': '123', 'password': '123'}

    result = schema.load(data)
    assert result is not None


def test_init():
    schema = UserSchema(only=['user_id'])

    assert schema is not None


def test_filtering_password():
    user = User(user_id='user123', password='123')
    schema = UserSchema(only=['user_id'])

    r = schema.dump(user)
    assert r is not None
    assert 'password' not in r


def test_dump_with_pk():
    user = User(user_id='user123', password='123')
    user.pk = '5f85469378ebc3de6b8cf152'

    schema = UserSchema(only=['user_id', '_id'])
    r = schema.dump(user)

    assert r is not None
    assert '_id' in r
