from flask.globals import request
from mongoengine.errors import ValidationError
from backend.schemas.like_schema import LikeSchema
from backend.services.like_service import LikeService
from flask_classful import FlaskView, route
from backend.views.decorators import deserialize, input_data_required, token_required


service = LikeService()
request_schema = LikeSchema()
response_schema = LikeSchema(many=True)


class LikesView(FlaskView):

    def index(self, **kwargs):
        content_id = request.args.get('contentId')
        content_type = request.args.get('contentType')
        result = service.get_likes(
            content_id, content_type)

        return {'result': [] if len(result) == 0 else response_schema.dump(result)}, 200

    @token_required
    @input_data_required
    @deserialize(request_schema)
    def post(self, **kwargs):
        auth_token, data = kwargs['auth_token'], kwargs['data']
        result = service.post_like(data, auth_token.user)

        if not result:
            return {'message': 'id does not exist'}, 404

        return {'result': result}, 201

    @token_required
    @input_data_required
    @deserialize(request_schema)
    def delete(self, **kwargs):
        auth_token, data = kwargs['auth_token'], kwargs['data']
        result = service.delete_like(data, auth_token.user)

        if not result:
            return {'message': 'id does not exist'}, 404

        return {'result': result}, 200
