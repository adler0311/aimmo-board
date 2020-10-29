import json

from backend.schemas.base import ResponseErrorSchema


def test_response_error_schema_dump():
    schema = ResponseErrorSchema()
    result = schema.dumps(404)

    assert result is not None
    data = json.loads(result)
    assert data['message'] == 'document matching id does not exist'
