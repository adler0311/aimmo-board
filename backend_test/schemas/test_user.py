from backend.models.user import User
from backend.schemas.user import UserLoadSchema, UserMarshalSchema


def test_load():
    schema = UserMarshalSchema()
    data = {'userId': '123', 'password': '123'}

    result = schema.load(data)
    assert result is not None


def test_init():
    schema = UserMarshalSchema(only=['user_id'])

    assert schema is not None


def test_filtering_password():
    user = User(user_id='user123', password='123')
    schema = UserMarshalSchema(only=['user_id'])

    r = schema.dump(user)
    assert r is not None
    assert 'password' not in r


def test_dump_with_pk():
    user = User(user_id='user123', password='123')
    user.pk = '5f85469378ebc3de6b8cf152'

    schema = UserMarshalSchema(only=['user_id', '_id'])
    r = schema.dump(user)

    assert r is not None
    assert '_id' in r

def test_user_load_schema_init():
    schema = UserLoadSchema()

    assert schema is not None