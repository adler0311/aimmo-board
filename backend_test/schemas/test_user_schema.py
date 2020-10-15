from backend.schemas.user_schema import UserSchema


def test_load():
    schema = UserSchema()
    data = {'userId': '123', 'password': '123'}

    result = schema.load(data)
    assert result is not None
