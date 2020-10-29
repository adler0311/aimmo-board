from mongoengine.base.fields import ObjectIdField
from backend.schemas.like import LikeSchema
from backend.models.like import Like


def test_init():
    schema = LikeSchema()

    assert schema is not None


def test_dump():
    schema = LikeSchema()
    l = Like(content_id=ObjectIdField('lf85469378ebc3de6b8cf152'))
    l.pk = "gf85469378ebc3de6b8cf152"

    result = schema.dump(l)

    assert result is not None
    assert result['_id'] is "gf85469378ebc3de6b8cf152"
